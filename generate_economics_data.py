import psycopg2
import random
from faker import Faker
from datetime import timedelta, date

fake = Faker()

SA_PROVINCES = ['Gauteng', 'Western Cape', 'KwaZulu-Natal',
                'Eastern Cape', 'Limpopo', 'Mpumalanga',
                'North West', 'Free State', 'Northern Cape']

INDICATORS = [
    ('GDP Growth Rate', '%'),
    ('Inflation Rate', '%'),
    ('Unemployment Rate', '%'),
    ('Repo Rate', '%'),
    ('Prime Lending Rate', '%'),
    ('Consumer Price Index', 'Index'),
    ('Exchange Rate USD/ZAR', 'ZAR'),
    ('Government Debt', 'Billion ZAR'),
    ('Foreign Direct Investment', 'Billion ZAR'),
    ('Trade Balance', 'Billion ZAR')
]

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="financial_intelligence_db",
        user="postgres",
        password="DcxzDrewDcxzD@91"
    )

def generate_indicators(conn):
    cursor = conn.cursor()
    print("Generating economic indicators...")

    start_date = date(2019, 1, 1)
    end_date = date(2024, 12, 31)
    current_date = start_date

    while current_date <= end_date:
        for indicator_name, unit in INDICATORS:
            if indicator_name == 'GDP Growth Rate':
                value = round(random.uniform(-3.5, 5.0), 2)
            elif indicator_name == 'Inflation Rate':
                value = round(random.uniform(3.0, 12.0), 2)
            elif indicator_name == 'Unemployment Rate':
                value = round(random.uniform(25.0, 35.0), 2)
            elif indicator_name == 'Repo Rate':
                value = round(random.uniform(3.5, 8.5), 2)
            elif indicator_name == 'Prime Lending Rate':
                value = round(random.uniform(7.0, 12.0), 2)
            elif indicator_name == 'Consumer Price Index':
                value = round(random.uniform(100.0, 160.0), 2)
            elif indicator_name == 'Exchange Rate USD/ZAR':
                value = round(random.uniform(14.0, 20.0), 2)
            elif indicator_name == 'Government Debt':
                value = round(random.uniform(3000, 5000), 2)
            elif indicator_name == 'Foreign Direct Investment':
                value = round(random.uniform(10, 100), 2)
            elif indicator_name == 'Trade Balance':
                value = round(random.uniform(-50, 50), 2)
            else:
                value = round(random.uniform(0, 100), 2)

            cursor.execute("""
                INSERT INTO economics.indicators
                (country, indicator_name, indicator_value, unit, recorded_date)
                VALUES (%s, %s, %s, %s, %s)
            """, ('South Africa', indicator_name, value, unit, current_date.strftime('%Y-%m-%d')))

        current_date += timedelta(days=30)

    conn.commit()
    print("Economic indicators generated successfully!")

if __name__ == "__main__":
    conn = get_connection()
    generate_indicators(conn)
    conn.close()
    print("All economics data generated successfully!")