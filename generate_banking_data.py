import psycopg2
import random
from faker import Faker
from datetime import timedelta

fake = Faker()

# South African specific data
SA_BANKS = ['Zwide Bank', 'Togu Financial', 'Mtimande Trust',
            'Ngwenya Credit', 'Faku Savings', 'Moshoeshoe Bank',
            'Gcaleka Financial']

SA_INSURERS = ['Mthembu Life', 'Solvent Assurance', 'Maliwa Insurance',
               'Sigcawu Life', 'Tlholego Assurance', 'Mazaleni Cover']

SA_AIRLINES = ['Mzamo Airways', 'Expo Air', 'Tempo Express',
               'Langa Air', 'Phalo Aviation']

SA_COMPANIES = ['Zwide Holdings', 'Togu Enterprises', 'Mtimande Group',
                'Ngwenya Solutions', 'Faku Trading', 'Malangana Corp',
                'Lawrence Industries', 'Livingstone Investments',
                'Gladstone Logistics', 'Nandi Retailers',
                'Ngconde Services', 'Lithemba Technologies',
                'Zodidi Consulting']

SA_LOAN_PROVIDERS = ['Ncobeni Credit', 'Mawawa Finance', 'Qendu Loans',
                     'Ngcwangu Capital', 'Brightness Fund']

SA_CITIES = ['Johannesburg', 'Cape Town', 'Pretoria', 'Durban',
             'Port Elizabeth', 'Bloemfontein', 'Soweto', 'Sandton',
             'Polokwane', 'Nelspruit']

ACCOUNT_TYPES = ['Cheque', 'Savings', 'Fixed Deposit', 'Money Market', 'Business']
ACCOUNT_STATUS = ['Active', 'Dormant', 'Closed', 'Suspended']
TRANSACTION_TYPES = ['Deposit', 'Withdrawal', 'Transfer', 'Payment',
                     'EFT', 'ATM', 'POS', 'Debit Order']
LOAN_TYPES = ['Home Loan', 'Vehicle Finance', 'Personal Loan',
              'Business Loan', 'Student Loan']
GENDERS = ['Male', 'Female']


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="financial_intelligence_db",
        user="postgres",
        password="DcxzDrewDcxzD@91"
    )


def generate_customers(conn, num_customers=500):
    cursor = conn.cursor()
    print(f"Generating {num_customers} customers...")

    for _ in range(num_customers):
        first_name = fake.first_name()
        last_name = fake.last_name()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d')
        gender = random.choice(GENDERS)
        email = fake.email()
        phone = '0' + str(random.randint(600000000, 899999999))
        city = random.choice(SA_CITIES)
        country = 'South Africa'

        cursor.execute("""
            INSERT INTO banking.customers 
            (first_name, last_name, date_of_birth, gender, email, phone, country, city)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, dob, gender, email, phone, country, city))

    conn.commit()
    print("Customers generated successfully!")


def generate_accounts(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM banking.customers")
    customers = [row[0] for row in cursor.fetchall()]
    print(f"Generating accounts for {len(customers)} customers...")

    for customer in customers:
        num_accounts = random.randint(1, 3)
        for _ in range(num_accounts):
            account_type = random.choice(ACCOUNT_TYPES)
            status = random.choices(ACCOUNT_STATUS, weights=[70, 15, 10, 5])[0]
            balance = round(random.uniform(100, 500000), 2)
            currency = 'ZAR'
            opened_date = fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d')

            cursor.execute("""
                INSERT INTO banking.accounts 
                (customer_id, account_type, account_status, balance, currency, opened_date)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (customer, account_type, status, balance, currency, opened_date))

    conn.commit()
    print("Accounts generated successfully!")


def generate_transactions(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT account_id FROM banking.accounts")
    accounts = [row[0] for row in cursor.fetchall()]
    print(f"Generating transactions for {len(accounts)} accounts...")

    for account in accounts:
        num_transactions = random.randint(5, 30)
        for _ in range(num_transactions):
            transaction_type = random.choice(TRANSACTION_TYPES)
            amount = round(random.uniform(50, 50000), 2)
            currency = 'ZAR'
            transaction_date = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
            description = f"{transaction_type} - {random.choice(SA_COMPANIES)}"
            status = random.choices(['Completed', 'Pending', 'Failed'], weights=[85, 10, 5])[0]

            cursor.execute("""
                INSERT INTO banking.transactions 
                (account_id, transaction_type, amount, currency, transaction_date, description, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (account, transaction_type, amount, currency, transaction_date, description, status))

    conn.commit()
    print("Transactions generated successfully!")


def generate_loans(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT customer_id FROM banking.customers")
    customers = [row[0] for row in cursor.fetchall()]
    print("Generating loans...")

    for customer in customers:
        if random.random() < 0.4:
            loan_type = random.choice(LOAN_TYPES)
            loan_amount = round(random.uniform(5000, 2000000), 2)
            interest_rate = round(random.uniform(7.5, 24.5), 2)
            start_date = fake.date_between(start_date='-3y', end_date='today').strftime('%Y-%m-%d')
            end_date = (fake.date_between(start_date='-3y', end_date='today') + timedelta(
                days=random.randint(365, 1825))).strftime('%Y-%m-%d')
            status = random.choices(['Active', 'Paid Up', 'Defaulted', 'Under Review'],
                                    weights=[60, 25, 10, 5])[0]

            cursor.execute("""
                INSERT INTO banking.loans 
                (customer_id, loan_type, loan_amount, interest_rate, start_date, end_date, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (customer, loan_type, loan_amount, interest_rate, start_date, end_date, status))

    conn.commit()
    print("Loans generated successfully!")


if __name__ == "__main__":
    conn = get_connection()
    generate_customers(conn)
    generate_accounts(conn)
    generate_transactions(conn)
    generate_loans(conn)
    conn.close()
    print("All banking data generated successfully!")