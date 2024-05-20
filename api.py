from flask import Flask, request, jsonify
import joblib
import pandas as pd
from libs import data_collector
app = Flask(__name__)



# Load the model and scaler
xgboost_model_WOD = joblib.load('./models/WOD/xgboost_model.joblib')
scaler_WOD = joblib.load('./models/WOD/scaler.joblib')

xgboost_model_7D = joblib.load('./models/7D/xgboost_model.joblib')
scaler_7D = joblib.load('./models/7D/scaler.joblib')

@app.route('/api/predict/WOD', methods=['GET'])
def predict_WOD():
    try:
        # Extract pair_id from the request
        pair_id = request.args.get('pair_id')
        
        if not pair_id:
            return jsonify({'error': 'pair_id is required'}), 400
        
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
            'prediction': int(prediction[0]),  # Predicted class (0 or 1)
            'score': float(prediction_score[0] * 100),  # Convert to percentage
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/api/predict/7D', methods=['GET'])
def predict_7D():
    try:
        # Extract pair_id from the request
        pair_id = request.args.get('pair_id')
        
        if not pair_id:
            return jsonify({'error': 'pair_id is required'}), 400
        
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
            'prediction': int(prediction[0]),  # Predicted class (0 or 1)
            'score': float(prediction_score[0] * 100),  # Convert to percentage
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
