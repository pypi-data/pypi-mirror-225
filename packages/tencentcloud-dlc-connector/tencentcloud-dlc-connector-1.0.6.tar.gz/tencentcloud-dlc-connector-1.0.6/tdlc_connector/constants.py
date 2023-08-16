

class Enum:

    @classmethod
    def ENUM_VALUES(cls):
        c = []
        for k, v in cls.__dict__.items():
            if not k.startswith('_'):
                c.append(v)
        return tuple(c)
    
    @classmethod
    def ENUM_KEYS(cls):
        c = []
        for k, v in cls.__dict__.items():
            if not k.startswith('_'):
                c.append(k)
        return tuple(c)


    @classmethod
    def ENUMS(cls):
        c = {}
        for k, v in cls.__dict__.items():
            if not k.startswith('_'):
                c[k] = v
        return c


class TaskStatus(Enum):

    INIT = 0
    RUNNING = 1
    SUCCESS = 2
    ERROR = -1
    KILL = -2


class SQLType(Enum):

    DDL = 'DDL'
    DML = 'DML'


class EngineType(Enum):

    SPARK = 'spark'
    PRESTO = 'presto'



class ResultStyles(Enum):

    LIST = 'list'
    TUPLE = 'tuple'
    DICT = 'dict'



class DataType(Enum):

    '''
    DLC:
    Hive:               https://cwiki.apache.org/confluence/display/Hive/LanguageManual+Types
    MySql:              https://dev.mysql.com/doc/refman/8.0/en/data-types.html
    MsSql:
    Postgres:
    Clickhouse: 
    '''

    #                                             |  DLC  | Spark | Presto | Hive | MySql | MsSql |  Clickhouse |
    # Numeric Data Types   [01 - 20]
    TINYINT                = 1          
    SMALLINT               = 2
    MEDIUMINT              = 3

    INT                    = 4
    INTEGER                = 5
    BIGINT                 = 6
    LONG                   = 7

    FLOAT                  = 8
    DOUBLE                 = 9
    DECIMAL                = 10


    # String Data Types    [21 - 40]
    CHAR                   = 21
    VARCHAR                = 22
    STRING                 = 23
    TINYTEXT               = 24
    TEXT                   = 25
    MEDIUMTEXT             = 26
    LONGTEXT               = 27
    TINYBLOB               = 28
    BLOB                   = 29
    MEDIUMBLOB             = 30
    LONGBLOB               = 31

    BINCHAR                = 32
    VARBINCHAR             = 33
    ENUM                   = 34
    # SET

    # Date Data Types      [41 - 60]
    DATE                   = 41
    TIME                   = 42
    YEAR                   = 43
    DATETIME               = 44
    TIMESTAMP              = 45


    # Other Data Types     [61 - ]
    JSON                   = 61
    BOOL                   = 62
    BOOLEAN                = 63
    ARRAY                  = 64
    MAP                    = 65
    STRUCT                 = 66
    # BINARY                 = 67


    # Spatial Data Types
    # GEOMETRY
    # POINT
    # LINESTRING
    # POLYGON
    # MULTIPOINT
    # MULTILINESTRING
    # MULTIPOLYGON
    # GEOMETRYCOLLECTION

    OTHER                  = 100


class Catalog:

    DATALAKECATALOG = 'DataLakeCatalog'
    # HIVE = 'hive'
    # EMR = 'emr'
    # POSTGRES = 'postgres'
    # MYSQL = 'mysql'
    # MSSQL = 'mssql'
    # CLICKHOUSE = 'clickhouse'



class FileSystem(Enum):

    COSN = 'cosn'
    LAKEFS = 'lakefs'



class CosKey(Enum):

    RESULT_META = 'meta/result.meta.json'
    RESULT_DATA = 'data'


class Mode(Enum):

    ALL = 'all'
    LASY = 'lasy'
    STREAM = 'stream'