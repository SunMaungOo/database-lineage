import urllib
from sqlalchemy import create_engine,text
from typing import Optional,List,Tuple,Any

type DatabaseResult = List[Tuple[Any,...]]

def get_connection_string(host:str,database_name:str,user:str,password:str,port:int=1433)->Optional[str]:

    driver = "{ODBC Driver 17 for SQL Server}"

    odbc_str = f"DRIVER={driver};SERVER={host};PORT={port};UID={user};DATABASE={database_name};PWD={password}"

    connection_string = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_str)}"

    return connection_string

def test_connection(connection_str:str)->bool:
    """
    Test whether we can connect to database
    """
    try:
        engine = create_engine(connection_str)

        with engine.connect() as connection:
            return True
    except:
        return False
    
def query(connection_str:str,query:str)->Optional[DatabaseResult]:
    
    try:
        engine = create_engine(connection_str)

        with engine.connect() as connection:
            result = connection.execute(text(query))

            return [tuple(row) for row in result]
    except:
        return None