import psycopg2

# --- Database Connection Parameters ---
connection_params = {
    'dbname': 'photon',
    'user': 'student',
    # 'password': 'student',
    # 'host': '/var/run/postgresql',  # use socket on Debian if needed
    # 'port': '5432'
}


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
    """Insert a new player, or update if the ID already exists."""
    conn, cursor = None, None
    try:
        conn = psycopg2.connect(**connection_params)
        cursor = conn.cursor()

        # First check if player exists
        cursor.execute("SELECT id FROM players WHERE id = %s;", (player_id,))
        exists = cursor.fetchone()

        if exists:
            # Update codename if player already exists
            cursor.execute(
                "UPDATE players SET codename = %s WHERE id = %s;",
                (codename, player_id)
            )
            print(f"[DB] Updated player {player_id}:{codename}")
        else:
            # Insert new player
            cursor.execute(
                "INSERT INTO players (id, codename) VALUES (%s, %s);",
                (player_id, codename)
            )
            print(f"[DB] Inserted player {player_id}:{codename}")

        conn.commit()

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


# --- Init with sample data ---
def init_players():
    """Insert John Fortnite and Jane Battlefield if they don’t exist."""
    starter_players = [
        (100, "John Fortnite"),
        (101, "Jane Battlefield"),
    ]
    for pid, cname in starter_players:
        add_player(pid, cname)


# --- Run standalone for testing ---
if __name__ == "__main__":
    init_players()
    print("Current players in DB:")
    for row in list_players():
        print(row)
