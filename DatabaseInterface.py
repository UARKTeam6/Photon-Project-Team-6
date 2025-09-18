import psycopg2
from psycopg2 import sql

connection_params = {
    'dbname': 'photon',
    'user': 'student',
    'password': 'student',
    'host': '127.0.0.1',
    'port': '5432'
}

try:
    conn = psycopg2.connect(**connection_params)
    cursor = conn.cursor()

    # execute query
    cursor.execute("SELECT version();")


    # fetch result
    version = cursor.fetchone()
    print(f"Connected to: {version}")

    cursor.execute('''
        INSERT INTO players (id, codename) 
        VALUES (%s, %s)        
                   ''', ('100', 'John fortnite'))
    cursor.execute('''
    INSERT INTO players (id, codename) 
    VALUES (%s, %s)
                    ''', ('101', 'Jane Battlefield'))
    conn.commit()

    cursor.execute('SELECT * FROM players;')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except Exception as error:
    print(f"Error connecting to PostgreSQL database: {error}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()

