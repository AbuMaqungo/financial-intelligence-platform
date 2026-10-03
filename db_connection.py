import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="financial_intelligence_db",
        user="postgres",
        password="DcxzDrewDcxzD@91"
    )
    return conn

if __name__ == "__main__":
    conn = get_connection()
    print("Connection successful!")
    conn.close()