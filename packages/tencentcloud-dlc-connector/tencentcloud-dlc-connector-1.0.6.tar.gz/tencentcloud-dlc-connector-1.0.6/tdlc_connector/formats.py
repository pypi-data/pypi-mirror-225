from datetime import datetime, date, time, timedelta
from time import localtime
from decimal import Decimal, getcontext
from typing import Sequence
from tdlc_connector import  exceptions, constants


import json
import re
import logging

LOG = logging.getLogger('Format')

# FORMAT_DATE = "{0.year:04}-{0.month:02}-{0.day:02}"
# FORMAT_TIME = "{0.hour:02}:{0.minute:02}:{0.second:02}"
# FORMAT_TIME_MILLISECOND = FORMAT_TIME + ".{0.microsecond:03}" # DLC 目前只支持到 millisecond
# FORMAT_DATETIME = FORMAT_DATE + " " + FORMAT_TIME
# FORMAT_DATETIME_MILLISECOND = FORMAT_DATE + " " + FORMAT_TIME_MILLISECOND

FORMAT_DATE = "%Y-%m-%d"
FORMAT_TIME = "%H:%M:%S"
FORMAT_TIME_MILLISECOND = FORMAT_TIME + ".%f" # DLC 目前只支持到 millisecond
FORMAT_DATETIME = FORMAT_DATE + " " + FORMAT_TIME
FORMAT_DATETIME_MILLISECOND = FORMAT_DATE + " " + FORMAT_TIME_MILLISECOND


'''
2022-09-23
2022-09-23 07:36:10
2022-09-23 07:36:10.123456
2022-09-23 07:36:10.123
2022-09-23T07:36:10
'''


DATETIME_REGEXP = re.compile(
    r"(\d{1,4})-(\d{1,2})-(\d{1,2})[T ](\d{1,2}):(\d{1,2}):(\d{1,2})(?:.(\d{1,6}))?"
)


# TODO  
# 当非 null 字段接受到 None 数据， 暂时不抛异常
def _isCompactNull(value):
    if value is None:
        return True
    if isinstance(value, str) and value == "":
        return True
    return False

def checkNull(fn):
   def fn_wrapper(value, *args, **kwargs):
        if _isCompactNull(value):
            value = None
        else:
            try:
                value = fn(value, *args, **kwargs)
            except Exception as e:
                LOG.warn(e)
        return value
   return fn_wrapper

def default_converter(value, *args, **kwargs):
    return value

@checkNull
def integer_converter(value, *args, **kwargs):
    return int(value)

@checkNull
def bigint_converter(value, *args, **kwargs): 
    return int(value)

def string_converter(value, *args, **kwargs):
    # TODO
    # 目前判断不出来 字符空 和 NULL
    return value

@checkNull
def decimal_converter(value, *args, **kwargs):
    return Decimal(value)

@checkNull
def float_converter(value, *args, **kwargs):
    return float(value)

@checkNull
def datetime_converter(value, *args, **kwargs):
    m = DATETIME_REGEXP.match(value)
    if m:
        format = FORMAT_DATETIME
        if m.group(7):
            format = FORMAT_DATETIME_MILLISECOND
        return datetime.strptime(value, format)

@checkNull
def date_converter(value, *args, **kwargs):
    return datetime.strptime(value, FORMAT_DATE)


@checkNull
def time_converter(value, *args, **kwargs):
    pass

@checkNull
def struct_converter(value, *args, **kwargs):
    return json.loads(value)

def array_converter(value, *args, **kwargs):
    pass



'''
TODO
python3 / 需要注意

DLC 支持 bigint/int    smallint/tinyint 会转化成 int
bigint      -2^63 (-9223372036854775808) 到 2^63-1 (9223372036854775807) 
int         -2^31 (-2,147,483,648) 到 2^31 - 1 (2,147,483,647)
smallint    -2^15 (-32,768) 到 2^15 - 1 (32,767)
tinyint     0 到 255 


date
timestamp  yyyy-mm-dd hh:mm:ss

'''


_TYPE_CODES = constants.DataType.ENUMS()

def getTypeCode(type_str):
    return _TYPE_CODES.get(type_str, constants.DataType.OTHER)


_CONVERTERS = {

    'INTEGER': integer_converter,
    'BIGINT': bigint_converter,
    'DECIMAL': decimal_converter,
    'DATE': date_converter,
    'TIMESTAMP': datetime_converter,
    'VARCHAR': string_converter,
    'STRING': string_converter,
    'FLOAT': float_converter,
    'DOUBLE': float_converter,

    # 不处理嵌套结构
    'STRUCT': struct_converter,

    # 'ARRAY'
    # 'MAP'

    'CHAR': string_converter
}

def getConvert(name):
    return _CONVERTERS.get(name.upper(), default_converter)

_trans = [chr(x) for x in range(128)]
_trans[ord("'")] = "\\'"

def string_literal(value: str):
    return "'" + value.translate(_trans) + "'"

def default_literal(value):
    return str(value)

def dict_literal(value: dict):
    n = {}
    for k, v in value.items():
        n[k] = literal(v)
    return n

def sequence_literal(value: Sequence):
    return "(" + ",".join([literal(item) for item in value]) + ")"

def set_literal(value: set):
    return  ",".join([literal(item) for item in value])

def datetime_literal(value: datetime):
    fmt = FORMAT_DATETIME
    if value.microsecond:
        fmt = FORMAT_DATETIME_MILLISECOND
    return "'" + value.strftime(fmt)  + "'"

def date_literal(value: date):
    return "'" + value.strftime(FORMAT_DATE) + "'"

_literals = {
    'int': default_literal,
    'str': string_literal,
    'dict': dict_literal,
    'list': sequence_literal,
    'tuple': sequence_literal,
    'set': set_literal,
    'date': date_literal,
    'datetime': datetime_literal,
#    'timestamp'
}

def literal(value):
    return _literals.get(type(value).__name__, default_literal)(value)




Date = date
Time = time
TimeDelta = timedelta
Timestamp = datetime


def DateFromTicks(ticks):
    return date(*localtime(ticks)[:3])


def TimeFromTicks(ticks):
    return time(*localtime(ticks)[3:6])


def TimestampFromTicks(ticks):
    return datetime(*localtime(ticks)[:6])


def Binary(x):
    return bytes(x)