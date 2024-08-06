import pyodbc

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=DESKTOP-E7TMHHH;'
        'DATABASE=python_crud;'
        'UID=sa;'
        'PWD=admin123;'
        'Encrypt=no;'
        'TrustServerCertificate=yes;'
    )
    return conn


