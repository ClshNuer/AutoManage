import pymysql

# Open database connection
with pymysql.connect(host='localhost', user='testuser', password='test123', database='TESTDB') as db:
    # Create a cursor object
    with db.cursor() as cursor:
        # Execute SQL query
        cursor.execute("SELECT VERSION()")

        # Fetch a single row
        data = cursor.fetchone()

        # Print the database version
        print(f"Database version: {data}")

