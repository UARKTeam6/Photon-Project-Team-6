import psycopg2

# --- Database Connection Parameters ---
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    # 'password': 'student',
    # 'host': 'localhost',
    # 'port': '5432'
}


# --- Initialization Function ---
def init_players():
    """Insert starter players if they don’t already exist."""
    conn, cursor = None, None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        starter_players = [
            (100, "John Fortnite"),
            (101, "Jane Battlefield")
        ]

        for pid, cname in starter_players:
            cursor.execute('''
                INSERT INTO players (id, codename)
                VALUES (%s, %s)
                ON CONFLICT (id) DO UPDATE SET codename = EXCLUDED.codename;
            ''', (pid, cname))

        conn.commit()
        print("[DB] Starter players added/ensured.")

    except Exception as error:
        print(f"[DB ERROR] {error}")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# --- Get Player by ID ---
def get_player(player_id):
    """Fetch codename for a given player_id. Returns None if not found."""
    conn, cursor = None, None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute("SELECT codename FROM players WHERE id = %s;", (player_id,))
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


# --- Add or Update Player ---
def add_player(player_id, codename):
    """Insert or update a player in the database."""
    conn, cursor = None, None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO players (id, codename)
            VALUES (%s, %s)
            ON CONFLICT (id) DO UPDATE SET codename = EXCLUDED.codename;
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


# --- List All Players ---
def list_players():
    """Return all players from the database as a list of tuples."""
    conn, cursor = None, None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        cursor.execute("SELECT id, codename FROM players ORDER BY id;")
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