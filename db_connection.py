import psycopg2

def get_connection():
    return psycopg2.connect("postgresql://financial_intelligence_29mn_user:fCAfT0YF7vsa78zBDlDWldCru5q1Ot7K@dpg-db2shkcs728c73agj7s0-a.frankfurt-postgres.render.com/financial_intelligence_29mn")

if __name__ == "__main__":
    conn = get_connection()
    print("Connection successful!")
    conn.close()