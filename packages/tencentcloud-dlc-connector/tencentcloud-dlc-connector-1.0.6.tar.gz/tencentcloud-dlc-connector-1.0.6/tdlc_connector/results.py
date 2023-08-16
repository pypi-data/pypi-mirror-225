from tdlc_connector import formats, constants, api, exceptions
import json
import urllib.parse
import re
import os
import csv
import tempfile
import logging

from qcloud_cos import cos_exception


LOG = logging.getLogger("Results")


class Column:

    def __init__(self, name, type, nullable, is_partition=False, precision=0, scale=0, comment=None) -> None:

        self.name = name
        self.type = type
        self.nullable = nullable
        self.is_partition = is_partition
        self.precision = precision
        self.scale = scale

        self._fn_type = formats.getConvert(self.type)
    
    def to(self, value):
        return self._fn_type(value, nullable=self.nullable, precision=self.precision, scale=self.scale)
    
REGEXP_ROWS = re.compile(r'\d+(?= rows affected)')



class ResultGenerator:

    def __init__(self, client: api.APIClient, statement_id, result_style, url, *args, **kwargs) -> None:

        self._client = client
        self._statement_id = statement_id
        self._result_style = result_style
        self._url = url

        self._columns = []

        self._handler = None

        if self._result_style == constants.ResultStyles.DICT:
            self._handler = lambda row: {self._columns[i].name:  self._columns[i].to(row[i]) for i in range(0, len(row))}
        else:
            self._handler = lambda row: tuple(self._columns[i].to(row[i]) for i in range(0, len(row)))
        

        self._initialize()
    
            
    @property
    def description(self):
        return tuple([(column.name, formats.getTypeCode(column.type), None, None, column.precision, column.scale, column.nullable) for column in self._columns])
    

    def _initialize(self, *args, **kwargs):
        pass

    def _iter_rows(self):
        pass

    @property
    def iterator(self):

        for row in self._iter_rows():
            yield self._handler(row)


class LasyRemoteResultGenerator(ResultGenerator):

    def __init__(self, client: api.APIClient, statement_id, result_style, url, *args, **kwargs) -> None:

        self._next_token = None
        self._results = []

        super().__init__(client, statement_id, result_style, url, *args, **kwargs)

    def _initialize(self):

        response = self._client.get_statement_results(self._statement_id)
        if response['state'] != constants.TaskStatus.SUCCESS:
            raise exceptions.ProgrammingError("Remote task state error.")

        for column in response['columns']:
            self._columns.append(Column(**column))


        self._next_token = response['next']
        self._results = response['results']

    
    def _iter_rows(self):

        for row in self._results:
            yield row

        next = self._next_token
        while next:
            response = self._client.get_statement_results(self._statement_id, next)
            if response['state'] != constants.TaskStatus.SUCCESS:
                raise exceptions.ProgrammingError("Remote task state error.")
            for row in response['results']:
                yield row
            next = response['next']
    

class RemoteResultGenerator(LasyRemoteResultGenerator):

    def _iter_rows(self):

        results = []
        
        for row in super()._iter_rows():
            results.append(row)

        for row in results:
            yield row


def parse_url(url):

    parser = urllib.parse.urlparse(url)

    scheme = parser.scheme
    netloc = parser.netloc
    path = parser.path

    bucket = netloc
    if scheme == constants.FileSystem.LAKEFS:
        _, bucket = netloc.split('@')

    return scheme, bucket, path.lstrip('/')


class LasyCOSResultGenerator(ResultGenerator):

    def __init__(self, client: api.APIClient, statement_id, result_style, path, *args, **kwargs) -> None:

        self._scheme = None
        self._bucket = None
        self._key = None

        super().__init__(client, statement_id, result_style, path, *args, **kwargs)


    def _initialize(self, *args, **kwargs):

        self._scheme, self._bucket, self._key = parse_url(self._url)

        if self._scheme == constants.FileSystem.LAKEFS:
            auth = self._client.get_lakefs_auth(self._url)
            self._client.patch_cos_client(auth['secretId'], auth['secretKey'], auth['token'])
        
        key = os.path.join(self._key, constants.CosKey.RESULT_META)

        if self._client.object_exists(self._bucket, key):
            stream = self._client.get_cos_object_stream(self._bucket, key)
            meta = json.load(stream)
            for column in meta['columns']:
                self._columns.append(Column(**column))


    def _iter_rows(self):

        prefix = os.path.join(self._key, constants.CosKey.RESULT_DATA)
        for item in self._client.iter_cos_objects(self._bucket, prefix):
            name = tempfile.mktemp(prefix=f"RESULT-{self._statement_id}")
            self._client.get_cos_object_stream_to_file(self._bucket, item['Key'], name)

            f = open(name, encoding='utf8')
            reader = csv.reader(f, escapechar='\\')
            next(reader) # skip header

            for line in reader:
                yield line

            f.close()
            os.remove(name)


class COSResultGenerator(LasyCOSResultGenerator):

    def _iter_rows(self):

        files = []
        prefix = os.path.join(self._key, constants.CosKey.RESULT_DATA)
        for item in self._client.iter_cos_objects(self._bucket, prefix):

            name = tempfile.mktemp(prefix=f"RESULT-{self._statement_id}")
            self._client.get_cos_object_stream_to_file(self._bucket, item['Key'], name)
            files.append(name)

        for file in files:

            reader = csv.reader(open(file), escapechar='\\')
            next(reader) # skip header
            for line in reader:
                yield line

            os.remove(file)


def iter_streaming_lines(stream):
    while True:
        line = stream.readline()
        if not line:
            break

        yield line.decode('utf8')


class StreamingCOSResultGenerator(LasyCOSResultGenerator):

        def _iter_rows(self):
            prefix = os.path.join(self._key, constants.CosKey.RESULT_DATA)
            for item in self._client.iter_cos_objects(self._bucket, prefix):
                stream = self._client.get_cos_object_stream(self._bucket, item['Key'])
                stream.readline() # skip header
                for line in csv.reader(iter_streaming_lines(stream), escapechar='\\'):
                    yield line


'''
ResultGenerator
RemoteResultGenerator
LasyRemoteResultGenerator

COSResultGenerator
LasyCOSResultGenerator
StreamingCOSResultGenerator      

'''

RESULT_GENERATORS = {
    'REMOTE_' + constants.Mode.ALL: RemoteResultGenerator,
    'REMOTE_' + constants.Mode.LASY: LasyRemoteResultGenerator,
    'REMOTE_' + constants.Mode.STREAM: LasyRemoteResultGenerator,

    'COS_' + constants.Mode.ALL: COSResultGenerator,
    'COS_' + constants.Mode.LASY: LasyCOSResultGenerator,
    'COS_' + constants.Mode.STREAM: StreamingCOSResultGenerator,
}