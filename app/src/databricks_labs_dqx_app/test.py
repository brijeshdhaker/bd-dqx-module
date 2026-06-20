import psycopg

try:
    connection = psycopg.connect(
        host="localhost", # or your remote server IP
        dbname="postgres",
        user="postgres",
        password="paSSW0rd",
        port="5432"
    )
    print("Connection successful!")
except Exception as error:
    print(f"Error connecting to the database: {error}")
finally:
    if connection:
        connection.close()

from psycopg_pool import ConnectionPool

# Initialize a global pool
pool = ConnectionPool(
    conninfo="dbname=test user=postgres password=secret host=localhost port=5432",
    min_size=2,
    max_size=10
)

# Use the pool safely with a context manager
def fetch_user_data(user_id):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT name FROM users WHERE id = %s;", (user_id,))
            return cur.fetchone()

# Close the pool when the application shuts down
# pool.close()