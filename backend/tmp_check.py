import mysql.connector
from creds import creds

con = None
try:
    con = mysql.connector.connect(
        host=creds.connectionstring,
        user=creds.username,
        password=creds.password,
        database=creds.database
    )
    print('CONNECTED')
    cur = con.cursor()
    cur.execute('SHOW TABLES')
    print(cur.fetchall())
    cur.execute('DESCRIBE floor')
    print(cur.fetchall())
    cur.execute('INSERT INTO floor (level, name) VALUES (%s, %s)', (1, 'First Floor'))
    con.commit()
    print('INSERT_OK')
except Exception as e:
    import traceback
    print(type(e).__name__, e)
    traceback.print_exc()
finally:
    if con is not None:
        con.close()
