import psycopg2
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

SA_INSURERS = ['Mthembu Life', 'Solvent Assurance', 'Maliwa Insurance',
               'Sigcawu Life', 'Tlholego Assurance', 'Mazaleni Cover']

SA_CITIES = ['Johannesburg', 'Cape Town', 'Pretoria', 'Durban',
             'Port Elizabeth', 'Bloemfontein', 'Soweto', 'Sandton',
             'Polokwane', 'Nelspruit']

POLICY_TYPES = ['Life Insurance', 'Vehicle Insurance', 'Home Insurance',
                'Medical Aid', 'Business Insurance', 'Funeral Cover',
                'Disability Cover', 'Travel Insurance']

CLAIM_STATUSES = ['Approved', 'Pending', 'Rejected', 'Under Review']
POLICY_STATUSES = ['Active', 'Lapsed', 'Cancelled', 'Expired']

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="financial_intelligence_db",
        user="postgres",
        password="DcxzDrewDcxzD@91"
    )

def generate_policies(conn, num_policies=300):
    cursor = conn.cursor()
    print(f"Generating {num_policies} policies...")

    for _ in range(num_policies):
        customer_name = fake.name()
        policy_type = random.choice(POLICY_TYPES)
        premium_amount = round(random.uniform(200, 15000), 2)
        coverage_amount = round(random.uniform(50000, 5000000), 2)
        start_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d')
        end_date = (fake.date_between(start_date='-5y', end_date='today') + timedelta(days=random.randint(365, 1825))).strftime('%Y-%m-%d')
        status = random.choices(POLICY_STATUSES, weights=[60, 15, 15, 10])[0]

        cursor.execute("""
            INSERT INTO insurance.policies
            (customer_name, policy_type, premium_amount, coverage_amount, start_date, end_date, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (customer_name, policy_type, premium_amount, coverage_amount, start_date, end_date, status))

    conn.commit()
    print("Policies generated successfully!")

def generate_claims(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT policy_id FROM insurance.policies")
    policies = [row[0] for row in cursor.fetchall()]
    print(f"Generating claims for {len(policies)} policies...")

    for policy in policies:
        if random.random() < 0.3:
            claim_date = fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
            claim_amount = round(random.uniform(1000, 500000), 2)
            claim_status = random.choices(CLAIM_STATUSES, weights=[50, 25, 15, 10])[0]
            description = f"Claim for {random.choice(['accident', 'theft', 'damage', 'medical', 'death', 'disability'])}"

            cursor.execute("""
                INSERT INTO insurance.claims
                (policy_id, claim_date, claim_amount, claim_status, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (policy, claim_date, claim_amount, claim_status, description))

    conn.commit()
    print("Claims generated successfully!")

if __name__ == "__main__":
    conn = get_connection()
    generate_policies(conn)
    generate_claims(conn)
    conn.close()
    print("All insurance data generated successfully!")