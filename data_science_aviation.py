import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
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
            airline,
            origin,
            destination,
            total_flights,
            total_passengers,
            total_revenue,
            total_fuel_cost,
            gross_profit,
            average_revenue
        FROM aviation.vw_flight_performance
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def prepare_data(df):
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    df['airline_encoded'] = le.fit_transform(df['airline'])
    df['origin_encoded'] = le.fit_transform(df['origin'])
    df['destination_encoded'] = le.fit_transform(df['destination'])

    features = ['airline_encoded', 'origin_encoded', 'destination_encoded',
                'total_flights', 'total_passengers', 'total_fuel_cost']

    X = df[features]
    y = df['gross_profit']

    return X, y, features, df

def train_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)

    # Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)

    print("=" * 50)
    print("RANDOM FOREST REGRESSOR RESULTS")
    print("=" * 50)
    print(f"R² Score:  {r2_score(y_test, rf_pred):.2f}")
    print(f"RMSE:      {np.sqrt(mean_squared_error(y_test, rf_pred)):,.2f}")
    print()
    print("=" * 50)
    print("LINEAR REGRESSION RESULTS")
    print("=" * 50)
    print(f"R² Score:  {r2_score(y_test, lr_pred):.2f}")
    print(f"RMSE:      {np.sqrt(mean_squared_error(y_test, lr_pred)):,.2f}")

    return rf_model, X_test, y_test, rf_pred, lr_pred

def plot_results(rf_model, X_test, y_test, rf_pred, lr_pred, features, df):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Aviation — Gross Profit Prediction', fontsize=16, fontweight='bold')

    # 1. Actual vs Predicted - Random Forest
    axes[0, 0].scatter(y_test, rf_pred, alpha=0.5, color='steelblue')
    axes[0, 0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                    'r--', linewidth=2)
    axes[0, 0].set_title('Random Forest — Actual vs Predicted')
    axes[0, 0].set_xlabel('Actual Gross Profit (ZAR)')
    axes[0, 0].set_ylabel('Predicted Gross Profit (ZAR)')

    # 2. Revenue by Airline
    revenue_by_airline = df.groupby('airline')['total_revenue'].sum().sort_values(ascending=True)
    revenue_by_airline.plot(kind='barh', ax=axes[0, 1], color='darkorange')
    axes[0, 1].set_title('Total Revenue by Airline')
    axes[0, 1].set_xlabel('Total Revenue (ZAR)')

    # 3. Feature Importance
    importances = rf_model.feature_importances_
    feat_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    feat_df = feat_df.sort_values('Importance', ascending=True)
    feat_df.plot(kind='barh', x='Feature', y='Importance', ax=axes[1, 0],
                color='steelblue', legend=False)
    axes[1, 0].set_title('Feature Importance — Random Forest')
    axes[1, 0].set_xlabel('Importance Score')

    # 4. Fuel Cost vs Gross Profit
    axes[1, 1].scatter(df['total_fuel_cost'], df['gross_profit'],
                       alpha=0.5, color='green')
    axes[1, 1].set_title('Fuel Cost vs Gross Profit')
    axes[1, 1].set_xlabel('Total Fuel Cost (ZAR)')
    axes[1, 1].set_ylabel('Gross Profit (ZAR)')

    plt.tight_layout()
    plt.savefig('aviation_gross_profit_prediction.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Chart saved as aviation_gross_profit_prediction.png")

if __name__ == "__main__":
    print("Loading aviation data from PostgreSQL...")
    df = load_data()
    print(f"Data loaded: {len(df)} records")

    print("Preparing data...")
    X, y, features, df = prepare_data(df)

    print("Training models...")
    rf_model, X_test, y_test, rf_pred, lr_pred = train_models(X, y)

    print("Generating visualisations...")
    plot_results(rf_model, X_test, y_test, rf_pred, lr_pred, features, df)

    print("Aviation Data Science complete!")