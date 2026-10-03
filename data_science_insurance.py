import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
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
            p.policy_type,
            p.premium_amount,
            p.coverage_amount,
            p.status as policy_status,
            COALESCE(c.claim_amount, 0) as claim_amount,
            CASE WHEN c.claim_id IS NOT NULL THEN 1 ELSE 0 END as has_claim,
            COALESCE(c.claim_status, 'No Claim') as claim_status
        FROM insurance.policies p
        LEFT JOIN insurance.claims c ON p.policy_id = c.policy_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def prepare_data(df):
    le = LabelEncoder()
    df['policy_type_encoded'] = le.fit_transform(df['policy_type'])
    df['policy_status_encoded'] = le.fit_transform(df['policy_status'])

    features = ['policy_type_encoded', 'policy_status_encoded',
                'premium_amount', 'coverage_amount']

    X = df[features]
    y = df['has_claim']

    return X, y, features, df

def train_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)

    lr_model = LogisticRegression(random_state=42)
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)

    print("=" * 50)
    print("RANDOM FOREST RESULTS")
    print("=" * 50)
    print(f"Accuracy:  {accuracy_score(y_test, rf_pred):.2f}")
    print(f"Precision: {precision_score(y_test, rf_pred, zero_division=0):.2f}")
    print(f"Recall:    {recall_score(y_test, rf_pred, zero_division=0):.2f}")
    print(f"F1 Score:  {f1_score(y_test, rf_pred, zero_division=0):.2f}")
    print()
    print("=" * 50)
    print("LOGISTIC REGRESSION RESULTS")
    print("=" * 50)
    print(f"Accuracy:  {accuracy_score(y_test, lr_pred):.2f}")
    print(f"Precision: {precision_score(y_test, lr_pred, zero_division=0):.2f}")
    print(f"Recall:    {recall_score(y_test, lr_pred, zero_division=0):.2f}")
    print(f"F1 Score:  {f1_score(y_test, lr_pred, zero_division=0):.2f}")

    return rf_model, X_test, y_test, rf_pred, lr_pred

def plot_results(rf_model, X_test, y_test, rf_pred, lr_pred, features, df):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Insurance — Claim Risk Scoring', fontsize=16, fontweight='bold')

    # 1. Confusion Matrix - Random Forest
    cm_rf = confusion_matrix(y_test, rf_pred)
    sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
    axes[0, 0].set_title('Random Forest — Confusion Matrix')
    axes[0, 0].set_xlabel('Predicted')
    axes[0, 0].set_ylabel('Actual')

    # 2. Claims by Policy Type
    claims_by_type = df.groupby('policy_type')['has_claim'].sum().sort_values(ascending=True)
    claims_by_type.plot(kind='barh', ax=axes[0, 1], color='steelblue')
    axes[0, 1].set_title('Total Claims by Policy Type')
    axes[0, 1].set_xlabel('Number of Claims')

    # 3. Feature Importance
    importances = rf_model.feature_importances_
    feat_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    feat_df = feat_df.sort_values('Importance', ascending=True)
    feat_df.plot(kind='barh', x='Feature', y='Importance', ax=axes[1, 0],
                 color='darkorange', legend=False)
    axes[1, 0].set_title('Feature Importance — Random Forest')
    axes[1, 0].set_xlabel('Importance Score')

    # 4. Premium vs Claim Amount
    axes[1, 1].scatter(df['premium_amount'], df['claim_amount'],
                       alpha=0.5, color='steelblue')
    axes[1, 1].set_title('Premium Amount vs Claim Amount')
    axes[1, 1].set_xlabel('Premium Amount (ZAR)')
    axes[1, 1].set_ylabel('Claim Amount (ZAR)')

    plt.tight_layout()
    plt.savefig('insurance_claim_risk_scoring.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Chart saved as insurance_claim_risk_scoring.png")

if __name__ == "__main__":
    print("Loading insurance data from PostgreSQL...")
    df = load_data()
    print(f"Data loaded: {len(df)} records")

    print("Preparing data...")
    X, y, features, df = prepare_data(df)

    print("Training models...")
    rf_model, X_test, y_test, rf_pred, lr_pred = train_models(X, y)

    print("Generating visualisations...")
    plot_results(rf_model, X_test, y_test, rf_pred, lr_pred, features, df)

    print("Insurance Data Science complete!")