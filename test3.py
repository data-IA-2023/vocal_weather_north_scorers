import pyodbc
from sqlalchemy import create_engine
import urllib

params = urllib.parse.quote_plus
(r'Driver={ODBC Driver 18 for SQL Server};Server=tcp:north-server.database.windows.net,1433;Database=North Data;Uid=Odin;Pwd=Valhalla1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
try:
    engine_azure = create_engine(conn_str,echo=True)
    print('connection is ok')
except:
    print('error')
