from flask import Flask, request, jsonify
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from libs import data_collector, features, uniswap_graphql, training
from xgboost import XGBClassifier

app = Flask(__name__)


@app.route('/api/predict/WOD', methods=['GET'])
def predict_WOD():
    try:
        try:
            xgboost_model_WOD = joblib.load('./models/WOD/xgboost_model.joblib')
            scaler_WOD = joblib.load('./models/WOD/scaler.joblib')
        except:
            print("Fail to load model and scaler")
            training.train('WOD')
            xgboost_model_7D = joblib.load('./models/WOD/xgboost_model.joblib')
            scaler_7D = joblib.load('./models/WOD/scaler.joblib')
            print("New model has trained")
        # Extract pair_id from the request
        pair_id = request.args.get('pair_id')
        pair = uniswap_graphql.pair_by_id(pair_id)
        if not pair_id:
            return jsonify({'error': 'pair_id is required'}), 400
        
        is_rugpull_occur, rugpull_timestamp = features.check_rugpull_by_liquidity_snapshots(pair_id=pair_id)
        if(is_rugpull_occur):
            return jsonify({
                'id': pair_id,
                'token0': pair['token0']['symbol'],
                'token1': pair['token1']['symbol'],
                'rug_pull-pull': True,
                'message': f'''Rug pull is already occured in this pair at: {rugpull_timestamp}''',
            })
            
        # Get the pair data using data_collection function
        pair_data = data_collector.pair_data_wod(pair_id)
        
        if not pair_data:
            return jsonify({'error': 'Failed to get data for pair_id'}), 400
        # Convert pair_data to DataFrame
        df = pd.DataFrame([pair_data])
        df = df.drop(columns=['label', 'id'])
        
        # Ensure the columns are in the correct order (same as the training data)
        expected_columns = [col for col in df.columns]
        df = df[expected_columns]
        
        # Scale the input data
        df_scaled = scaler_WOD.transform(df)
        
        # Predict using the loaded model
        prediction_score = xgboost_model_WOD.predict_proba(df_scaled)[:, 1]  # Probability of positive class
        prediction = xgboost_model_WOD.predict(df_scaled)
        # Return the prediction as JSON
        return jsonify({
            'id': pair_id,
            'token0': pair['token0']['symbol'],
            'token1': pair['token1']['symbol'],
            'rug_pull': True if int(prediction[0]) == 1 else False,  # Predicted class (0 or 1)
            'score': float(prediction_score[0] * 100),  # Convert to percentage
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/api/predict/7D', methods=['GET'])
def predict_7D():
    try:
        try:
            xgboost_model_7D = joblib.load('./models/7D/xgboost_model.joblib')
            scaler_7D = joblib.load('./models/7D/scaler.joblib')
        except:
            print("Fail to load model and scaler")
            training.train(method='7D')
            xgboost_model_7D = joblib.load('./models/7D/xgboost_model.joblib')
            scaler_7D = joblib.load('./models/7D/scaler.joblib')
            print("New model has trained")
        # Extract pair_id from the request
        pair_id = request.args.get('pair_id')
        pair = uniswap_graphql.pair_by_id(pair_id)
        
        if not pair_id:
            return jsonify({'error': 'pair_id is required'}), 400
        
        is_rugpull_occur, rugpull_timestamp = features.check_rugpull_by_liquidity_snapshots(pair_id=pair_id)
        if(is_rugpull_occur):
            return jsonify({
                'id': pair_id,
                'token0': pair['token0']['symbol'],
                'token1': pair['token1']['symbol'],
                'rug_pull-pull': True,
                'message': f'Rug pull is already occured in this pair at: {rugpull_timestamp}',
            })
        
        # Get the pair data using data_collection function
        pair_data = data_collector.pair_data_7d(pair_id)
        
        if not pair_data:
            return jsonify({'error': 'Failed to get data for pair_id'}), 400
        
        # Convert pair_data to DataFrame
        df = pd.DataFrame([pair_data])
        df = df.drop(columns=['label', 'id'])
        
        # Ensure the columns are in the correct order (same as the training data)
        expected_columns = [col for col in df.columns]
        df = df[expected_columns]
        
        # Scale the input data
        df_scaled = scaler_7D.transform(df)
        
        # Predict using the loaded model
        prediction_score = xgboost_model_7D.predict_proba(df_scaled)[:, 1]  # Probability of positive class
        prediction = xgboost_model_7D.predict(df_scaled)
        
        # Return the prediction as JSON
        return jsonify({
            'id': pair_id,
            'token0': pair['token0']['symbol'],
            'token1': pair['token1']['symbol'],
            'prediction': int(prediction[0]),  # Predicted class (0 or 1)
            'score': float(prediction_score[0] * 100),  # Convert to percentage
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/train/WOD', methods=['POST'])
def train_WOD():
    try:
        training.train('WOD')
        
        return jsonify({'message': 'Model WOD has been trained and exported'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/api/train/7D', methods=['POST'])
def train_7D():
    try:
        training.train(method='7D')        
        return jsonify({'message': 'Model 7D has been trained and exported'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
if __name__ == '__main__':
    app.run(debug=True)
