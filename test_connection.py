import mysql.connector

db_config = {
    'user': 'root',
    'password': '94Gry610@',
    'host': '127.0.0.1',
    'database': 'student_db'
}

try:
    conn = mysql.connector.connect(**db_config)
    print("Connection successful!")
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if conn.is_connected():
        conn.close()
