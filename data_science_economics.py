import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import numpy as np
import warnings

warnings.filterwarnings('ignore')


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="financial_intelligence_db",
        user="postgres",
        password="DcxzDrewDcxzD@91"
    )


def load_data():
    conn = get_connection()
    query = """
        SELECT 
            indicator_name,
            unit,
            year,
            average_value,
            min_value,
            max_value
        FROM economics.vw_indicators_summary
        ORDER BY indicator_name, year
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def plot_results(df):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('South Africa — Economic Indicators Analysis & Forecasting',
                 fontsize=16, fontweight='bold')

    # 1. GDP Growth Rate Over Time
    gdp = df[df['indicator_name'] == 'GDP Growth Rate'].copy()
    gdp['year_num'] = pd.to_datetime(gdp['year']).dt.year
    axes[0, 0].plot(gdp['year_num'], gdp['average_value'],
                    marker='o', color='steelblue', linewidth=2)
    axes[0, 0].axhline(y=0, color='red', linestyle='--', alpha=0.5)
    axes[0, 0].set_title('GDP Growth Rate Over Time (%)')
    axes[0, 0].set_xlabel('Year')
    axes[0, 0].set_ylabel('GDP Growth Rate (%)')
    axes[0, 0].grid(True, alpha=0.3)

    # 2. Inflation vs Repo Rate
    inflation = df[df['indicator_name'] == 'Inflation Rate'].copy()
    repo = df[df['indicator_name'] == 'Repo Rate'].copy()
    inflation['year_num'] = pd.to_datetime(inflation['year']).dt.year
    repo['year_num'] = pd.to_datetime(repo['year']).dt.year
    axes[0, 1].plot(inflation['year_num'], inflation['average_value'],
                    marker='o', color='red', linewidth=2, label='Inflation Rate')
    axes[0, 1].plot(repo['year_num'], repo['average_value'],
                    marker='s', color='steelblue', linewidth=2, label='Repo Rate')
    axes[0, 1].set_title('Inflation Rate vs Repo Rate (%)')
    axes[0, 1].set_xlabel('Year')
    axes[0, 1].set_ylabel('Rate (%)')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # 3. Unemployment Rate Over Time
    unemployment = df[df['indicator_name'] == 'Unemployment Rate'].copy()
    unemployment['year_num'] = pd.to_datetime(unemployment['year']).dt.year
    axes[1, 0].bar(unemployment['year_num'], unemployment['average_value'],
                   color='darkorange', alpha=0.8)
    axes[1, 0].set_title('Unemployment Rate Over Time (%)')
    axes[1, 0].set_xlabel('Year')
    axes[1, 0].set_ylabel('Unemployment Rate (%)')
    axes[1, 0].grid(True, alpha=0.3, axis='y')

    # 4. USD/ZAR Exchange Rate Forecast
    forex = df[df['indicator_name'] == 'Exchange Rate USD/ZAR'].copy()
    forex['year_num'] = pd.to_datetime(forex['year']).dt.year

    # Linear regression forecast
    X = forex['year_num'].values.reshape(-1, 1)
    y = forex['average_value'].values
    model = LinearRegression()
    model.fit(X, y)

    # Forecast next 3 years
    future_years = np.array([2025, 2026, 2027]).reshape(-1, 1)
    forecast = model.predict(future_years)

    axes[1, 1].plot(forex['year_num'], forex['average_value'],
                    marker='o', color='steelblue', linewidth=2, label='Actual')
    axes[1, 1].plot([2025, 2026, 2027], forecast,
                    marker='s', color='red', linewidth=2,
                    linestyle='--', label='Forecast')
    axes[1, 1].set_title('USD/ZAR Exchange Rate Forecast')
    axes[1, 1].set_xlabel('Year')
    axes[1, 1].set_ylabel('Exchange Rate (ZAR)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    r2 = r2_score(y, model.predict(X))
    print(f"Exchange Rate Forecast Model R² Score: {r2:.2f}")
    print(f"Forecasted USD/ZAR: 2025={forecast[0]:.2f}, 2026={forecast[1]:.2f}, 2027={forecast[2]:.2f}")

    plt.tight_layout()
    plt.savefig('economics_indicators_forecast.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Chart saved as economics_indicators_forecast.png")


if __name__ == "__main__":
    print("Loading economics data from PostgreSQL...")
    df = load_data()
    print(f"Data loaded: {len(df)} records")

    print("Generating economic analysis and forecasts...")
    plot_results(df)

    print("Economics Data Science complete!")