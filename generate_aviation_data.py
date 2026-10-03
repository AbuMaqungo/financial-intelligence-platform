import psycopg2
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

SA_AIRLINES = ['Mzamo Airways', 'Expo Air', 'Tempo Express',
               'Langa Air', 'Phalo Aviation']

SA_AIRPORTS = ['Johannesburg OR Tambo', 'Cape Town International',
               'Durban King Shaka', 'Pretoria Wonderboom',
               'Port Elizabeth', 'Bloemfontein', 'Lanseria']

INTERNATIONAL_AIRPORTS = ['London Heathrow', 'Dubai International',
                          'New York JFK', 'Nairobi Jomo Kenyatta',
                          'Doha Hamad', 'Frankfurt', 'Amsterdam Schiphol']

AIRCRAFT_TYPES = ['Boeing 737', 'Boeing 747', 'Airbus A320',
                  'Airbus A330', 'Embraer E190', 'Boeing 787']

FLIGHT_STATUSES = ['Completed', 'Cancelled', 'Delayed', 'On Time']


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="financial_intelligence_db",
        user="postgres",
        password="DcxzDrewDcxzD@91"
    )


def generate_aircraft(conn):
    cursor = conn.cursor()
    print("Generating aircraft...")

    for airline in SA_AIRLINES:
        num_aircraft = random.randint(3, 8)
        for _ in range(num_aircraft):
            aircraft_type = random.choice(AIRCRAFT_TYPES)
            capacity = random.choice([120, 150, 180, 220, 300, 350])
            manufacture_year = random.randint(2000, 2023)
            status = random.choices(['Active', 'Maintenance', 'Retired'],
                                    weights=[75, 20, 5])[0]

            cursor.execute("""
                INSERT INTO aviation.aircraft
                (airline, aircraft_type, capacity, manufacture_year, status)
                VALUES (%s, %s, %s, %s, %s)
            """, (airline, aircraft_type, capacity, manufacture_year, status))

    conn.commit()
    print("Aircraft generated successfully!")


def generate_flights(conn, num_flights=1000):
    cursor = conn.cursor()
    print(f"Generating {num_flights} flights...")

    all_airports = SA_AIRPORTS + INTERNATIONAL_AIRPORTS

    for _ in range(num_flights):
        airline = random.choice(SA_AIRLINES)
        origin = random.choice(SA_AIRPORTS)
        destination = random.choice(all_airports)

        while destination == origin:
            destination = random.choice(all_airports)

        flight_date = fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
        passengers = random.randint(50, 350)
        revenue = round(random.uniform(50000, 2000000), 2)
        fuel_cost = round(revenue * random.uniform(0.25, 0.40), 2)

        cursor.execute("""
            INSERT INTO aviation.flights
            (airline, origin, destination, flight_date, passengers, revenue, fuel_cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (airline, origin, destination, flight_date, passengers, revenue, fuel_cost))

    conn.commit()
    print("Flights generated successfully!")


if __name__ == "__main__":
    conn = get_connection()
    generate_aircraft(conn)
    generate_flights(conn)
    conn.close()
    print("All aviation data generated successfully!")