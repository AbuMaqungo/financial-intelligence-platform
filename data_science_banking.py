import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, \
    classification_report
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
            c.gender,
            c.city,
            a.account_type,
            a.balance,
            l.loan_type,
            l.loan_amount,
            l.interest_rate,
            l.status as loan_status
        FROM banking.loans l
        JOIN banking.customers c ON l.customer_id = c.customer_id
        JOIN banking.accounts a ON c.customer_id = a.customer_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def prepare_data(df):
    # Create target variable — 1 = Defaulted, 0 = Not Defaulted
    df['defaulted'] = (df['loan_status'] == 'Defaulted').astype(int)

    # Encode categorical columns
    le = LabelEncoder()
    df['gender_encoded'] = le.fit_transform(df['gender'])
    df['city_encoded'] = le.fit_transform(df['city'])
    df['account_type_encoded'] = le.fit_transform(df['account_type'])
    df['loan_type_encoded'] = le.fit_transform(df['loan_type'])

    # Features and target
    features = ['gender_encoded', 'city_encoded', 'account_type_encoded',
                'loan_type_encoded', 'loan_amount', 'interest_rate', 'balance']

    X = df[features]
    y = df['defaulted']

    return X, y, features


def train_models(X, y):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)

    # Logistic Regression
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

    return rf_model, lr_model, X_test, y_test, rf_pred, lr_pred, X_train


def plot_results(rf_model, X_test, y_test, rf_pred, lr_pred, features, X_train):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Banking — Loan Default Prediction', fontsize=16, fontweight='bold')

    # 1. Confusion Matrix - Random Forest
    cm_rf = confusion_matrix(y_test, rf_pred)
    sns.heatmap(cm_rf, annot=True, fmt='d', cmap='Blues', ax=axes[0, 0])
    axes[0, 0].set_title('Random Forest — Confusion Matrix')
    axes[0, 0].set_xlabel('Predicted')
    axes[0, 0].set_ylabel('Actual')

    # 2. Confusion Matrix - Logistic Regression
    cm_lr = confusion_matrix(y_test, lr_pred)
    sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Oranges', ax=axes[0, 1])
    axes[0, 1].set_title('Logistic Regression — Confusion Matrix')
    axes[0, 1].set_xlabel('Predicted')
    axes[0, 1].set_ylabel('Actual')

    # 3. Feature Importance
    importances = rf_model.feature_importances_
    feat_df = pd.DataFrame({'Feature': features, 'Importance': importances})
    feat_df = feat_df.sort_values('Importance', ascending=True)
    feat_df.plot(kind='barh', x='Feature', y='Importance', ax=axes[1, 0], color='steelblue', legend=False)
    axes[1, 0].set_title('Feature Importance — Random Forest')
    axes[1, 0].set_xlabel('Importance Score')

    # 4. Model Accuracy Comparison
    models = ['Random Forest', 'Logistic Regression']
    accuracies = [
        accuracy_score(y_test, rf_pred),
        accuracy_score(y_test, lr_pred)
    ]
    axes[1, 1].bar(models, accuracies, color=['steelblue', 'darkorange'])
    axes[1, 1].set_title('Model Accuracy Comparison')
    axes[1, 1].set_ylabel('Accuracy Score')
    axes[1, 1].set_ylim(0, 1)
    for i, v in enumerate(accuracies):
        axes[1, 1].text(i, v + 0.01, f'{v:.2f}', ha='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig('banking_loan_default_prediction.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("Chart saved as banking_loan_default_prediction.png")


if __name__ == "__main__":
    print("Loading data from PostgreSQL...")
    df = load_data()
    print(f"Data loaded: {len(df)} records")

    print("Preparing data...")
    X, y, features = prepare_data(df)

    print("Training models...")
    rf_model, lr_model, X_test, y_test, rf_pred, lr_pred, X_train = train_models(X, y)

    print("Generating visualisations...")
    plot_results(rf_model, X_test, y_test, rf_pred, lr_pred, features, X_train)

    print("Banking Data Science complete!")