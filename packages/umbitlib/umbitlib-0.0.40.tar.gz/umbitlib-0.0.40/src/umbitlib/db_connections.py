# Package Imports
import keyring as kr
import psycopg2
import cx_Oracle
import pandas as pd
import time
from typing import Any, Optional, Tuple, Union
from warnings import filterwarnings
filterwarnings("ignore")
import importlib

from umbitlib.helpers import convert_seconds


# Security Functions
###################################################################################################
def import_conn_vars():
    """
    Imports the necessary security file containing database parameters for use in connecting 
    to Orcale or Postgres.

    Returns:
        db_conn_vars file
    """
    import sys
    try:
        sys.path.append("\\\\ad.utah.edu\\uuhc\\umb2\\shared\\Analytics Team\\Security")
        import db_conn_vars
        return db_conn_vars
    except Exception as e:
        print(f"{e}: Security file not found.")
        pass


def get_credential_keyring(service_name: str, username: str) -> Tuple[str, str]:
    """
    Retrieves a credential for a given service and username from the keyring.

    Parameters:
        service_name (str): The name of the service associated with the credentials.
        username (str): The username for which the credentials are retrieved.

    Returns:
        Tuple[str, str]: A tuple containing the username and password retrieved from the keyring.

    Example:
        user, pw = get_credential_keyring(service_name='postgres_dev', username=None)
    """
    try:
        security_obj = kr.get_credential(service_name=service_name, username=username)
        retrieved_username = security_obj.username
        password = security_obj.password
        return retrieved_username, password
    except:
        raise ReferenceError("Specified Keyring credential not found. For assistance in setting up Keyring credentials view: \nhttps://wiki.data.med.utah.edu/en/Analytics/Data-Science/Docs/Keyring-and-Setting-Credentials")
    


# Postgres Connection Functions
###################################################################################################
def postgres_select_db_params(destination: str) -> Tuple[str, str, int]:
    """
    Selects the PostgreSQL database parameters based on the destination.

    Parameters:
        destination (str): The target destination, which should be one of {'dev', 'prod'}.

    Returns:
        Tuple[str, str, int]: A tuple containing the database name, host, and port corresponding to the destination.
        
    Raises:
        ValueError: If the destination is not 'dev' or 'prod'.
    """   
    destination=destination.lower() 
    valid_destinations = {'dev', 'prod'}
    if destination not in valid_destinations:
        raise ValueError(f"destination must be one of {valid_destinations}")
    
    security_info = import_conn_vars() 
    
    if destination == 'dev':
        db = security_info.PG_DEV_DB
        host = security_info.PG_DEV_HOST
        port = security_info.PG_DEV_PORT
    elif destination == 'prod':
        db = security_info.PG_PROD_DB
        host = security_info.PG_PROD_HOST
        port = security_info.PG_PROD_PORT

    return db, host, port


def postgres_connect(username: str, password: str, destination: str = 'dev', conn_success_msg: bool = True) -> Any:
    """
    Creates a connection to a PostgreSQL database.  Requires that the programmer closes the connection in a separate statment.

    Parameters:
        username (str): The PostgreSQL username.
        password (str): The password for the PostgreSQL user.
        destination (str, optional): The target PostgreSQL database name (default is 'dev').
        conn_success_msg (bool, optional): If True, prints connection success message (default is False).

    Returns:
        Union[pd.DataFrame, None]: The result of the executed query as a DataFrame, or None if the query fails.
    
    Example:
        user, pw = get_credential_keyring(service_name='postgres_dev', username=None)
        postgres_conn = postgres_connect(username=user, password=pw, destination='dev', conn_success_msg=True)
        *** your code here ***
        postgres_conn.close
    """    
    db, host, port = postgres_select_db_params(destination=destination)            

    try:
        postgres_connection = psycopg2.connect(
            user=username,
            password=password,
            host=host,
            port=port,
            database=db
        )

        if conn_success_msg:
            print(f"Connection to Postgres {destination} for user {username} via Keyring: Successful")

        return postgres_connection

    except Exception as e:
        print(f"Connection to Postgres {destination} via Keyring: Failed - Error {e}")


def postgres_connect_query_close(username: str, password: str, destination: str = 'dev', conn_success_msg: bool = True,
               query_success_msg: bool = True) -> Any:
    """
    A constructor function that instantiates a query function into which sql can be passed and executed against the
    Postgres database.  

    Parameters:
        username (str): The PostgreSQL username.
        password (str): The password for the PostgreSQL user.
        destination (str, optional): The target PostgreSQL database name (default is 'dev').
        conn_success_msg (bool, optional): If True, prints connection success message (default is False).
        query_success_msg (bool, optional): If True, prints query success message (default is False).

    Returns:
        Union[pd.DataFrame, None]: The result of the executed query as a DataFrame, or None if the query fails.

    Example:
        user, pw = get_credential_keyring(service_name='postgres_dev', username=None)
        postgres_query = postgres_connect_query_close(username=user, password=pw, destination='dev', conn_success_msg=True, query_success_msg=True)
        df = postgres_query('your sql string here')   
    """    
    db, host, port = postgres_select_db_params(destination=destination)            

    def query_postgres(sql: Optional[str] = None) -> Union[pd.DataFrame, None]:
        try:
            postgres_connection = psycopg2.connect(
                user=username,
                password=password,
                host=host,
                port=port,
                database=db
            )

            if conn_success_msg:
                print(f"Connection to Postgres {destination} for user {username} via Keyring: Successful")

            try:
                tic = time.perf_counter()
                df = pd.read_sql_query(sql, postgres_connection)            
                postgres_connection.close() 
                toc = time.perf_counter()            

                if query_success_msg:
                    elapsed_time = toc - tic
                    days, hours, minutes, seconds = convert_seconds(elapsed_time)
                    print(f"Query executed without error in {days}d:{hours}h:{minutes}m:{round(seconds,2)}s.")
                return df            

            except Exception as e:
                print(f"Postgres query against {destination} for user {username} failed to run: Error {e}")

        except Exception as e:
            print(f"Connection to Postgres {destination} via Keyring: Failed - Error {e}") 

    return query_postgres


# Oracle Connection Function
###################################################################################################
def oracle_connect(username: str, password: str, conn_success_msg: bool = True) -> Any:
    """
    Creates a connection to an Oracle database.  Requires that the programmer closes the connection in a separate statment.

    Parameters:
        username (str): The Oracle username.
        password (str): The password for the Oracle user.
        conn_success_msg (bool, optional): If True, prints connection success message (default is False).
        query_success_msg (bool, optional): If True, prints query success message (default is False).

    Returns:
        Union[pd.DataFrame, None]: The result of the executed query as a DataFrame, or None if the query fails.

    Example:
        user, pw = get_credential_keyring(service_name='oracle', username=None)
        oracle_conn = oracle_connect(username=user, password=pw, conn_success_msg=True)
        *** your code here ***
        oracle_conn.close
    """
    security_info = import_conn_vars() 
    db = security_info.ODB_NAME
    
    try:
        oracle_connection = cx_Oracle.connect(
            username,
            password,
            db
        )

        if conn_success_msg:
                print(f"Connection to Oracle for user {username} via Keyring: Successful")

        return oracle_connection

    except Exception as e:
            print(f"Connection to Oracle via Keyring: Failed - Error {e}")


def oracle_connect_query_close(username: str, password: str, conn_success_msg: bool = True,
                      query_success_msg: bool = True) -> Any:
    """
    A constructor function that instantiates a query function into which sql can be passed and executed against the
    Oracle database.

    Parameters:
        username (str): The Oracle username.
        password (str): The password for the Oracle user.
        conn_success_msg (bool, optional): If True, prints connection success message (default is False).
        query_success_msg (bool, optional): If True, prints query success message (default is False).

    Returns:
        Union[pd.DataFrame, None]: The result of the executed query as a DataFrame, or None if the query fails.
    
    Example:
        user, pw = get_credential_keyring(service_name='oracle', username=None)
        oracle_query = oracle_connect_query_close(username=user, password=pw, conn_success_msg=True, query_success_msg=True)
        df = oracle_query('your sql string here')
    """
    security_info = import_conn_vars() 
    db = security_info.ODB_NAME
    
    def query_oracle(sql: Optional[str] = None) -> Union[pd.DataFrame, None]:
        try:
            oracle_connection = cx_Oracle.connect(
                username,
                password,
                db
            )

            if conn_success_msg:
                print(f"Connection to Oracle for user {username} via Keyring: Successful")

            try:
                tic = time.perf_counter()
                df = pd.read_sql_query(sql, oracle_connection)
                oracle_connection.close()
                toc = time.perf_counter()

                if query_success_msg:
                    elapsed_time = toc - tic
                    days, hours, minutes, seconds = convert_seconds(elapsed_time)
                    print(f"Query executed without error in {days}d:{hours}h:{minutes}m:{round(seconds,2)}s.")
                return df

            except Exception as e:
                print(f"Query against Oracle for user {username} failed to run: Error {e}")

        except Exception as e:
            print(f"Connection to Oracle via Keyring: Failed - Error {e}")

    return query_oracle 