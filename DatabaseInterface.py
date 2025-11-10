# DatabaseInterface.py
import psycopg2
from psycopg2.extras import RealDictCursor

# --- Robust connection helper ---
def _connect():
    # 1) Try Debian's default Unix socket first
    try:
        conn = psycopg2.connect(
            dbname="photon",
            user="student",
            host="/var/run/postgresql",  # Debian default socket dir
        )
        conn.autocommit = True
        return conn
    except Exception as e1:
        print(f"[DB DEBUG] Socket connect failed: {e1}")

    # 2) Fallback to TCP localhost (requires md5 in pg_hba.conf)
    try:
        conn = psycopg2.connect(
            dbname="photon",
            user="student",
            password="student",          # set this to your actual password if used
            host="127.0.0.1",
            port="5432",
        )
        conn.autocommit = True
        return conn
    except Exception as e2:
        print(f"[DB DEBUG] TCP connect failed: {e2}")
        raise

# --- Get Player by ID ---
def get_player(player_id):
    try:
        with _connect() as conn, conn.cursor() as cur:
            # ensure we’re on public schema
            cur.execute("SET search_path TO public;")
            cur.execute("SELECT codename FROM players WHERE id = %s;", (player_id,))
            row = cur.fetchone()
            return row[0] if row else None
    except Exception as error:
        print(f"[DB ERROR get_player] {error}")
        return None

# --- Add or Update Player ---
def add_player(player_id, codename):
    try:
        with _connect() as conn, conn.cursor() as cur:
            cur.execute("SET search_path TO public;")
            cur.execute("SELECT 1 FROM players WHERE id = %s;", (player_id,))
            if cur.fetchone():
                cur.execute(
                    "UPDATE players SET codename = %s WHERE id = %s;",
                    (codename, player_id)
                )
                print(f"[DB] Updated player {player_id}:{codename}")
            else:
                cur.execute(
                    "INSERT INTO players (id, codename) VALUES (%s, %s);",
                    (player_id, codename)
                )
                print(f"[DB] Inserted player {player_id}:{codename}")

            # sanity check: confirm it’s there
            cur.execute("SELECT id, codename FROM players WHERE id = %s;", (player_id,))
            print(f"[DB CHECK] Row now: {cur.fetchone()}")
            return True
    except Exception as error:
        print(f"[DB ERROR add_player] {error}")
        return False

def list_players():
    try:
        with _connect() as conn, conn.cursor() as cur:
            cur.execute("SET search_path TO public;")
            cur.execute("SELECT id, codename FROM players ORDER BY id;")
            return cur.fetchall()
    except Exception as error:
        print(f"[DB ERROR list_players] {error}")
        return []
