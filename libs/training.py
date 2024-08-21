import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from xgboost import XGBClassifier

def train(method: str):
    dataframe = pd.read_csv(f'''./datasets/Dataset_{method}.csv''')
    # Preprocess the data
    label_encoder = LabelEncoder()
    dataframe.dropna(inplace=True)
    dataframe.rename(columns=lambda x: x.lower(), inplace=True)
    dataframe['label'] = label_encoder.fit_transform(dataframe['label'])

    # Split data into features and labels
    x = dataframe.drop(columns=['id', 'label'], axis=1)
    y = dataframe['label']

    # Scale the features
    scaler = StandardScaler().fit(x)
    x_scaled = pd.DataFrame(scaler.transform(x))

    # Train the model
    xgboost_model = XGBClassifier(objective="binary:logistic", n_estimators=20, random_state=42, eval_metric=["auc", "error", "error@0.6"])
    xgboost_model.fit(x_scaled, y)

    # Save the model and scaler
    joblib.dump(xgboost_model, f'''./models/{method}/xgboost_model.joblib''')
    joblib.dump(scaler, f'./models/{method}/scaler.joblib')