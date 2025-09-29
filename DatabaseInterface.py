import psycopg2
from psycopg2 import sql

# Define connection parameters
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    #'password': 'student',
    #'host': 'localhost',
    #'port': '5432'
}

def get_player(player_id):
    """Fetch codename for a given player_id. Returns None if not found."""
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute("SELECT codename FROM players WHERE player_id = %s;", (player_id,))
        row = cursor.fetchone()
        return row[0] if row else None

    except Exception as error:
        print(f"[DB ERROR] {error}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def add_player(player_id, codename):
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO players (player_id, codename)
            VALUES (%s, %s)
            ON CONFLICT (player_id) DO UPDATE SET codename = EXCLUDED.codename;
        ''', (player_id, codename))
        conn.commit()
        print(f"[DB] Added/updated player {player_id}:{codename}")
    except Exception as error:
        print(f"[DB ERROR] {error}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def list_players():
    """Return all players from the database as a list of tuples."""
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute("SELECT player_id, codename FROM players ORDER BY player_id;")
        rows = cursor.fetchall()
        return rows

    except Exception as error:
        print(f"[DB ERROR] {error}")
        return []

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
