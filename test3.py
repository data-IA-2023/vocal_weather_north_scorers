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

def virgule(a):
    b=""
    for carac in a:
        if carac==',' or carac== ';':
            b+=' , '
        else:
            b+=carac
    return b
def underscore(a):
    a=' '.join(a)
    b=''
    for carac in a:
        if carac=='_':
            b+=''
        else:
            b+=carac
    b=b.lower()
    b=b.split(' ')
    return b
def localisation(a,b):
    a=a.lower()
    a=virgule(a)
    a=a.split(' ')
    b=underscore(b)
    c=[]
    for i in range(len(a)):
        if a[i] in b:
            if i!=0 and a[i-1] in b:
                c[-1]=c[-1]+' '+a[i]
            else:
                c.append(a[i])
    return c

print(localisation('il fait beau ici a Tours , mais à st Cyr sur loire, Paris non',['Tours','St','cyr','sur','loire','paris']))
