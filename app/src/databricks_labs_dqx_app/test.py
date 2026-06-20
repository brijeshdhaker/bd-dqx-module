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