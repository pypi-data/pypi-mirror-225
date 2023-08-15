import unittest
import keyring as kr
import psycopg2
import cx_Oracle

from src.umbitlib import db_connections

import sys
sys.path.append("\\\\ad.utah.edu\\uuhc\\umb2\\shared\\Analytics Team\\Security")
import db_conn_vars


class TestImportConnVars(unittest.TestCase): 

    def test_import_conn_vars(self):
        """
        Checks to see that db_conn_vars is not empty upon import
        """
        dcv = db_connections.import_conn_vars()
        message = "Test value is not none."
        self.assertIsNotNone(dcv, message)


class TestGetCredentialKeyring(unittest.TestCase):    

    def test_check_credential(self):
        """
        Test to see that pulled credenital matches the set credential        
        """
        # set test credential
        sname = 'test_serv'
        uname = 'test_user'
        pname = 'test_pass'
        kr.set_password(service_name=sname, username=uname, password=pname)
        
        user, pw = db_connections.get_credential_keyring(service_name=sname, username=None)
        self.assertEqual([user, pw], [uname, pname])
        

class TestPostgresSelectDbParams(unittest.TestCase):

    def test_check_dev_params(self):
        test_db = db_conn_vars.PG_DEV_DB
        test_host = db_conn_vars.PG_DEV_HOST
        test_port = db_conn_vars.PG_DEV_PORT
        db, host, port = db_connections.postgres_select_db_params(destination="dev")
        self.assertEqual([db, host, port], [test_db, test_host, test_port])

    def test_check_prod_params(self):
        test_db = db_conn_vars.PG_PROD_DB
        test_host = db_conn_vars.PG_PROD_HOST
        test_port = db_conn_vars.PG_PROD_PORT
        db, host, port = db_connections.postgres_select_db_params(destination="prod")
        self.assertEqual([db, host, port], [test_db, test_host, test_port])


class TestPostgresConnect(unittest.TestCase):

    def test_postgres_dev_connect(self):
        """
        Test that a connection object is successfully created
        """
        user, pw = db_connections.get_credential_keyring(service_name='postgres_dev', username=None)
        conn = db_connections.postgres_connect(username=user, password=pw, destination='dev')
        self.assertIsNotNone(conn)
    
    def test_postgres_prod_connect(self):
        """
        Test that a connection object is successfully created
        """
        user, pw = db_connections.get_credential_keyring(service_name='postgres_prod', username=None)
        conn = db_connections.postgres_connect(username=user, password=pw, destination='prod')
        self.assertIsNotNone(conn)


# class TestPostgresConnectQueryClose(unittest.TestCase):

    def test_postgres_dev_connect_query_close(self):
        """
        Test that a connection object is successfully created
        """
        query = """
                SELECT *
                FROM PUBLIC.HUB_ACTION
                WHERE ACTION_ID = 3001
                """
        user, pw = db_connections.get_credential_keyring(service_name='postgres_dev', username=None)
        postgres_query = db_connections.postgres_connect_query_close(username=user, password=pw, destination='dev')
        df = postgres_query(query)
        self.assertEqual(df['action_name'][0], 'Created')

    def test_postgres_prod_connect_query_close(self):
        """
        Test that a connection object is successfully created
        """
        query = """
                SELECT *
                FROM PUBLIC.HUB_ACTION
                WHERE ACTION_ID = 3001
                """
        user, pw = db_connections.get_credential_keyring(service_name='postgres_prod', username=None)
        postgres_query = db_connections.postgres_connect_query_close(username=user, password=pw, destination='prod')
        df = postgres_query(query)
        self.assertEqual(df['action_name'][0], 'Created')

        
class TestOracleConnect(unittest.TestCase):

    def test_oracle_connect(self):
        """
        Test that a connection object is successfully created
        """
        user, pw = db_connections.get_credential_keyring(service_name='oracle', username=None)
        conn = db_connections.oracle_connect(user, pw)
        self.assertIsNotNone(conn)


class TestOracleConnectQueryClose(unittest.TestCase):

    def test_oracle_connect(self):
        """
        Test that a connection object is successfully created
        """
        query = """
                SELECT NAME
                FROM CLARITY_REPORT.ZC_STATE
                WHERE ABBR = 'AK'
                """
        user, pw = db_connections.get_credential_keyring(service_name='oracle', username=None)
        oracle_query = db_connections.oracle_connect_query_close(user, pw)
        df = oracle_query(query)
        self.assertEqual(df['NAME'][0], 'Alaska')

