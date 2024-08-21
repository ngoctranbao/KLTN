import joblib
import pandas as pd
from libs import data_collector, features, uniswap_graphql
import json
import argparse

# Load the model and scaler
xgboost_model_WOD = joblib.load('./models/WOD/xgboost_model.joblib')
scaler_WOD = joblib.load('./models/WOD/scaler.joblib')

xgboost_model_7D = joblib.load('./models/7D/xgboost_model.joblib')
scaler_7D = joblib.load('./models/7D/scaler.joblib')

def predict_rugpull(pair_id, model, scaler, data_function):
    try:
        pair = uniswap_graphql.pair_by_id(pair_id)
        
        if not pair:
            print("Invalid pair_id. Please check and try again.")
            return
        
        # Check if rug-pull has already occurred
        is_rugpull_occur, rugpull_timestamp = features.check_rugpull_by_liquidity_snapshots(pair_id=pair_id)
        if is_rugpull_occur:
            print(json.dumps({
                'id': pair_id,
                'token0': pair['token0']['symbol'],
                'token1': pair['token1']['symbol'],
                'rug_pull': True,
                'message': f'Rug pull has already occurred in this pair at: {rugpull_timestamp}'
            }, indent=1))
            return
            
        # Get the pair data using data_collection function
        pair_data = data_function(pair_id)
        
        if not pair_data:
            print(f'Failed to get data for pair_id: {pair_id}')
            return
        
        # Convert pair_data to DataFrame
        df = pd.DataFrame([pair_data])
        df = df.drop(columns=['label', 'id'])
        
        # Ensure the columns are in the correct order (same as the training data)
        expected_columns = df.columns.tolist()  # Get the list of columns
        df = df[expected_columns]
        
        # Scale the input data
        df_scaled = scaler.transform(df)
        # Predict using the loaded model
        prediction_score = model.predict_proba(df_scaled)[:, 1]  # Probability of positive class
        prediction = model.predict(df_scaled)
        
        # Print the prediction result
        print(json.dumps({
            'id': pair_id,
            'token0': pair['token0']['symbol'],
            'token1': pair['token1']['symbol'],
            'rug_pull': True if int(prediction[0]) == 1 else False,  # Predicted class (0 or 1)
            'score': float(prediction_score[0] * 100),  # Convert to percentage
        }, indent=1))
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rugpull Prediction Program')
    parser.add_argument('--method', type=str, choices=['WOD', '7D'], required=True, help='Model to use for prediction (WOD or 7D)')
    parser.add_argument('--pair_id', type=str, required=True, help='Pair ID to predict rugpull status')

    args = parser.parse_args()

    if args.method == 'WOD':
        predict_rugpull(args.pair_id, xgboost_model_WOD, scaler_WOD, data_collector.pair_data_wod)
    elif args.method == '7D':
        predict_rugpull(args.pair_id, xgboost_model_7D, scaler_7D, data_collector.pair_data_7d)
    else:
        print("Invalid model choice. Please enter 'WOD' or '7D'.")
