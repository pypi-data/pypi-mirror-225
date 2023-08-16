from tencentcloud.common.profile import http_profile, client_profile
from tencentcloud.common.credential import Credential
from tencentcloud.dlc.v20210125 import models, dlc_client

from tdlc_connector import api, results, constants, cursors, exceptions

import time
import re
import logging

LOG = logging.getLogger("Connection")

REGEXP_ROWS = re.compile(r'\d+(?= rows affected)')

class DlcConnection:

    def __init__(self,
            *,
            region=None,
            secret_id=None,
            secret_key=None,
            token=None,
            endpoint=None,
            catalog=constants.Catalog.DATALAKECATALOG,
            engine="public-engine",
            engine_type=constants.EngineType.PRESTO,
            result_style=constants.ResultStyles.LIST,
            download=False,
            mode=constants.Mode.ALL,
            polling_interval=0.5,
            config={}
            ) -> None:

        if not region:
            raise exceptions.ProgrammingError("region is required.")
        
        if not secret_id:
            raise exceptions.ProgrammingError("secret-id is required.")

        if not secret_key:
            raise exceptions.ProgrammingError("secret-key is required.")
        
        if not engine:
            raise exceptions.ProgrammingError("engine is required.")
        
        if engine_type not in constants.EngineType.ENUM_VALUES():
            raise exceptions.ProgrammingError(f"Argument engine_type='{engine_type}' is not valid.")

        if result_style not in constants.ResultStyles.ENUM_VALUES():
            raise exceptions.ProgrammingError(f"Argument result_type='{result_style}' is not valid.")
        
        mode = mode.lower()
        if mode not in constants.Mode.ENUM_VALUES():
            raise exceptions.ProgrammingError(f"Argument mode='{mode}' is not valid.")
        
        if not download and mode == constants.Mode.STREAM:
            LOG.warn("'stream' mode is only supported when download=True, using 'lasy' mode instead.")
            mode = constants.Mode.LASY

        self._engine = engine
        self._catalog = catalog
        self._loop_interval = polling_interval
        self._result_style = result_style
        self._download = download
        self._mode = mode
        self._config = config


        self._engine_type = engine_type
        if engine is None:
            self._engine_type = constants.ENGINE_TYPE_PRESTO
        
        self._client = api.APIClient(region, secret_id, secret_key, token, endpoint)

    def open(self):
        pass

    def close(self):
        pass

    def connect(self):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

    def cursor(self):
        return cursors.Cursor(self)


    def execute_statement(self, statement):

        statement_id = self._client.submit_statement(self._engine, self._engine_type, self._catalog, statement, self._config)
        path = None
        message = ''

        while True:
            response = self._client.get_statement(statement_id)

            if response["state"] == constants.TaskStatus.KILL:
                raise exceptions.OperationalError(f"The task[{statement_id}] is killed.")

            if response["state"] == constants.TaskStatus.ERROR:
                raise exceptions.ProgrammingError(response["message"])
            
            if response["state"] == constants.TaskStatus.SUCCESS:
                path = response['path']
                message = response['rowAffectInfo']
                break
            
            time.sleep(self._loop_interval)
    


        prefix = 'REMOTE_'
        if self._download:
            prefix = 'COS_'
    
        name = prefix + self._mode

        g = results.RESULT_GENERATORS[name](self._client, statement_id, self._result_style, path)

        r = REGEXP_ROWS.findall(message)
        total = 0
        if r:
            total = int(r[0])

        return total, g.description, g.iterator