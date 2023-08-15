import sqlalchemy as sa
import pyodbc
import urllib.parse
import polars as pl
from urllib import parse
import traceback
import re


class SQLConnectionPolars:
    """ Connect to Microsoft SQL """

    def __init__(self, server_creds, wincred=False, master=False):
        """ Initialize the class
        -----------------------------
        server_creds = {
                        "server_name": "saassqltst-1.database.windows.net",
                        "db_name": "dw",
                        "user_name": "DSapps_AnLuMaSe",
                        "password": "L$nKZV3w!x7PP$+zDL@dNqbt9m++Qdgx3Cg77GmVqTthn+q?@f"
                        }
        wincred = False
        master = False

        con_ = SQLConnection(server_creds, wincred, master)
        -----------------------------
        :param server_creds: Dictionary containing the info to connect to the Server
        :param wincred: Indicate whether the connection to SQL will be done via Windows Authentication or not
        :param master: Indicate whether the connection will be done to master or to a specific database
        """

        self.wincred = wincred
        self.master = master

        drivers = [driver for driver in pyodbc.drivers() if (bool(re.search(r'\d', driver)))]
        self.driver = drivers[0]
        self.server = server_creds['server_name']
        self.user_name = server_creds['user_name']
        self.password = server_creds['password']

        if ~self.master:
            self.db_name = server_creds['db_name']

        self.con = None
        self.engine = None
        self.con_string = None

        driver_attempt = False
        iindex = 0
        while driver_attempt is False:
            try:
                self.query('''SELECT TOP 1 * FROM information_schema.tables;''')
                driver_attempt = True
            except:
                iindex += 1
                if iindex >= len(drivers):
                    raise ValueError(
                        "There are no valid drivers in the system to connect to the database: %s" % self.db_name)
                else:
                    self.driver = drivers[iindex]

    def open_read_connection(self):
        """ Open a reading connection with the Server
        :return: The opened connection
        """
        if self.wincred:
            if self.master:
                self.con_string = 'mssql+pyodbc://' + self.user_name + ':%s@' + self.server + '/master' + \
                    '?driver=' + parse.quote_plus(self.driver) + '&trusted_connection=yes'
            else:
                self.con_string = 'mssql://' + self.user_name + ':%s@' + self.server + '/' + self.db_name + \
                                  '?driver=' + parse.quote_plus(self.driver) + '&trusted_connection=yes'
        else:
            self.con_string = 'mssql+pyodbc://' + self.user_name + ':%s@' + self.server + '/' + self.db_name + \
                        '?driver=' + parse.quote_plus(self.driver)

        self.con_string = self.con_string % parse.quote_plus(self.password)
        self.engine = sa.create_engine(self.con_string)
        self.con = self.engine.connect().connection

    def open_write_connection(self):
        """ Open a writing connection with the Server
        :return: The opened connection
        """
        # driver = 'SQL+Server'
        constring = 'mssql+pyodbc://' + self.user_name + ':%s@' + self.server + '/' + self.db_name + \
                    '?driver=' + self.driver
        self.engine = sa.create_engine(constring % parse.quote_plus(urllib.parse.quote_plus(self.password)))
        self.con = self.engine.connect().connection

    def close_connection(self):
        """ Close any opened connections with the Server
        :return: None
        """
        self.con.close()
        if self.engine:
            self.engine.dispose()

    @staticmethod
    def _chunker(seq, size):
        """ Split the data set in chunks to be sent to SQL
                :param seq: Sequence of records to be split
                :param size: Size of any of the chunks to split the data
                :return: The DataFrame divided in chunks
                """
        return (seq[pos:pos + size] for pos in range(0, len(seq), size))

    def query(self, sql_query, coerce_float=False):
        """ Read data from SQL according to the sql_query
        -----------------------------
        query_str = "SELECT * FROM %s" & table
        con_.query(query_str)
        -----------------------------
        :param sql_query: Query to be sent to SQL
        :param coerce_float: Attempt to convert values of non-string, non-numeric objects (like decimal.Decimal)
        to floating point.
        :return: DataFrame gathering the requested data
        """
        self.open_read_connection()
        data = None
        try:
            data = pl.read_sql(sql=sql_query, connection_uri=self.con_string)
        except ValueError:
            print(traceback.format_exc())
        finally:
            self.close_connection()
        return data

    @staticmethod
    def _parse_df(parse, data, col_names):
        """  Auxiliar function to convert list to DataFrame
        :param parse: Parameter to indicate whether the data has to be transformed into a DataFrame or not
        :param data: List gathering the data retrieved from SQL
        :param col_names: List of columns to create the DataFrame
        :return: Formatted data
        """
        if parse is True:
            col_names = list(zip(*list(col_names)))[0]
            res = pl.DataFrame(list(zip(*data)), index=col_names).T
        else:
            res = [col_names, data]
        return res

    def sp_results(self, sql_query, resp_number=None, parse=True):
        """ Execute a stored procedure and retrieves all its output data
        -----------------------------
        query_str = "EXECUTE %s" & stored_procedure
        con_.sp_results(query_str, resp_number=1)
        -----------------------------
        :param sql_query: Query to be sent to SQL
        :param resp_number: Indicate which of the stored procedures responses will be retrieved
        :param parse: Indicate whether the output needs to be converted to a DataFrame or not
        :return: DataFrame list gathering the requested data
        """
        self.open_read_connection()
        data_list = list()
        cursor = None
        try:
            cursor = self.con.cursor()
            cursor.execute(sql_query)
            if resp_number is not None:
                for cursor_number in range(resp_number - 1):
                    cursor.nextset()
                try:
                    data_list.append(self._parse_df(parse, cursor.fetchall(), cursor.description))
                except ValueError:
                    raise ValueError('Please indicate a valid resp_number')
            else:
                aux_cursor = True
                count = 0
                while aux_cursor is not False and count < 100:
                    try:
                        data_list.append(self._parse_df(parse, cursor.fetchall(), cursor.description))
                        aux_cursor = cursor.nextset()
                    except Exception as e:
                        cursor.nextset()
                    finally:
                        count += 1
                    if count >= 100:
                        raise RuntimeError("Method sp_results has loop over 100 times for database '%s' on server '%s'"
                                           % (self.db_name, self.server))
            self.con.commit()
        except ValueError:
            print(traceback.format_exc())
        finally:
            if cursor:
                cursor.close()
            self.close_connection()
        return data_list
