import mysql.connector 
from mysql.connector import Error

def DBConnection(hname, uname, passd, dbname):
    con=None
    try:
        con=mysql.connector.connect(
            host=hname,
            user=uname,
            password= passd,
            database = dbname
        )
        print("DB connection successful")
    except Error as e:
        print("Error is:", e)
    return con

def execute_read_query(con, query, params=None):
    """Execute a SELECT query with optional parameters for safe queries"""
    cursor = con.cursor(dictionary=True)
    allrows = None
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        allrows = cursor.fetchall()
        return allrows
    except Error as e:
        print("Error is:", e)
        return []

def execute_query(con, query, params=None):
    """Execute INSERT/UPDATE/DELETE query with optional parameters for safe queries"""
    # Return the real error message to the API layer when a write fails
    if con is None:
        print("Database connection is not available")
        return False, "Database connection is not available"

    cursor = con.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        con.commit()
        print("DB is updated")
        return True, None
    except Error as e:
        con.rollback()
        print("Error is:", e)
        return False, str(e)
    except Exception as e:
        if con is not None:
            con.rollback()
        print("Error is:", e)
        return False, str(e)
    finally:
        cursor.close()
