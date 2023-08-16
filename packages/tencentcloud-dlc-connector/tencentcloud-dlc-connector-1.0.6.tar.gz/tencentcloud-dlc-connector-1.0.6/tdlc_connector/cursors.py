from tdlc_connector import formats, exceptions
import re
import logging


LOG = logging.getLogger('Cursor')


REGEXP_INSERT_VALUES = re.compile(
    r"\s*((?:INSERT)\b.+\bVALUES?\s*)"
    + r"(\(\s*(?:%s|%\(.+\)s)\s*(?:,\s*(?:%s|%\(.+\)s)\s*)*\))",
    re.IGNORECASE | re.DOTALL,
)

MAX_STATEMENT_LENGTH = 1024 * 1024 * 2

class Cursor:

    def __init__(self, connection) -> None:

        self.description = None
        self.rowcount = -1
        self.arraysize = 1

        self.connection = connection
        self.iterator = None

        self._executed = False

    
    def __del__(self):

        self.close()

    def close(self):
        pass
    
    def setinputsizes(self, *args):
        """Does nothing, required by DB API."""

    def setoutputsizes(self, *args):
        """Does nothing, required by DB API."""

    def reset(self):

        self.rowcount = -1
        self.arraysize = 1
        self.description = None
        self.iterator = None

        self._executed = False

    def _escape_args(self, args=None):
        if isinstance(args, (tuple, list)):
            return tuple([formats.literal(item) for item in args])
        elif isinstance(args, dict):
            return {k: formats.literal(v) for (k, v) in args.items()}
        return formats.literal(args)

    def execute(self, statement, args=None):

        if args is not None:
            statement = statement % self._escape_args(args)

        try:
            self.rowcount, self.description, self.iterator = self.connection.execute_statement(statement)
        except exceptions.ProgrammingError:
            raise
        except Exception as e:
            raise exceptions.ProgrammingError(e)

        self._executed = True
        return self.rowcount

    def executemany(self, statement, args):
        if not args:
            return

        m = REGEXP_INSERT_VALUES.match(statement)
        rows = 0

        if m:
            LOG.debug("[executemany] using bulk insert.")
            prefix = m.group(1)
            values = m.group(2).rstrip()
            # TODO 这里 prefix 直接超长会有异常

            query = prefix
            for arg in args:
                v = values % self._escape_args(arg)
                if len(query) + len(v) + 1 > MAX_STATEMENT_LENGTH:
                    rows += self.execute(query.rstrip(','))
                    query = prefix
                query += v + ','
            rows += self.execute(query.rstrip(','))
        else:
            LOG.debug("[executemany] using loop.")
            rows += sum(self.execute(statement, arg) for arg in args)
        
        self.rowcount = rows
        return self.rowcount

    def callproc(self, procname, args=()):
        """ optional """
        pass

    def assert_executed(self):
        if not self._executed:
            raise exceptions.ProgrammingError("Please execute SQL first. ")

    def fetchone(self):

        self.assert_executed()

        value = None
        if not self.iterator:
            return value
        
        try:
            value = next(self.iterator)
        except StopIteration:
            pass
        except Exception:
            raise
        return value

    def fetchmany(self, size=None):

        self.assert_executed()

        values = []
        if not self.iterator:
            return tuple(values)

        take = size or self.arraysize or 1

        for value in self.iterator:
            values.append(value)
            take -= 1
            if take <= 0:
                break

        return tuple(values)

    def fetchall(self):

        self.assert_executed()

        values = []
        if not self.iterator:
            return tuple(values)

        for value in self.iterator:
            values.append(value)
        return tuple(values)

    def nextset(self):
        pass
