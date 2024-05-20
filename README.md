# Rug-Pull Prediction Program

This program predicts the likelihood of a rug-pull event occurring in a given liquidity pool on the Uniswap platform. The prediction is based on historical data and machine learning models trained specifically for this purpose.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Models and Features](#models-and-features)
- [Examples](#examples)

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/rug-pull-prediction.git
    cd rug-pull-prediction
    ```
2. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

# Usage
The program can be run as a console application. It requires specifying the prediction method (WOD or 7D) and the pair ID.

## Running the predictor program
```
python predict.py --method METHOD --pair_id PAIR_ID
```

- `METHOD`: The prediction model to use (`WOD` for short-term prediction or `7D` for longer-term prediction).
- `PAIR_ID`: The ID of the Uniswap pair to predict.

#### Examples
To predict with the WOD method:
```bash
python predict.py --method WOD --pair_id 0x3eb09d108d1f61f10860b8bb1b13b5b4abc3f49d
```
Output:
```
Fetching pair data for pair_id: 0x3eb09d108d1f61f10860b8bb1b13b5b4abc3f49d
Fetching transactions (mints, burns, swaps)...
Fetching token info...
Fetching LP holders...
Calculating features...
Fetching data success!
{
 "id": "0x3eb09d108d1f61f10860b8bb1b13b5b4abc3f49d",
 "token0": "GROW",
 "token1": "WETH",
 "rug_pull": false,
 "score": 9.667453914880753
}
```
To predict with the 7D method:
```bash
python predict.py --method 7D --pair_id 0x3eb09d108d1f61f10860b8bb1b13b5b4abc3f49d
```
Output:
```
Fetching pair data for pair_id: 0x3eb09d108d1f61f10860b8bb1b13b5b4abc3f49d
Fetching transactions (mints, burns, swaps)...
Fetching token info...
Fetching LP holders...
Calculating features...
Fetching data success!
{
 "id": "0x3eb09d108d1f61f10860b8bb1b13b5b4abc3f49d",
 "token0": "GROW",
 "token1": "WETH",
 "rug_pull": false,
 "score": 9.667453914880753
}
```

## Data collection program
```
Input: ./datasets/Pairs.csv

Output: ./datasets/WOD.csv
        ./datasets/7D.csv
```

### Run the program
Requires:
```
python3 data_collection_7D.py
python3 data_collection_WOD.py
```
or
```
bash data_collection.bash
```

## Training model program
Requires
```
Input:  ./datasets/WOD.csv
        ./datasets/7D.csv
Output: ./models/WOD.csv
        ./models/7D.csv
```
### Run the program

```
python3 training_7D.py
python3 training_WOD.py
```

or

```
bash training.bash
```

## Using the API
The program also provides RESTful APIs for making predictions.
Run api
```
python3 api.py
```

#### Predict Rug-pull using WOD method
**Endpoint:** /api/predict/WOD
**Method**: GET

**Query Parameters:**

- pair_id: The ID of the Uniswap pair to predict.

**Example:**
```
curl -X GET "http://localhost:5000/api/predict/WOD?pair_id=0x3eb09d108d1f61f10860b8bb1b13b5b4abc3f49d"
```
Response:
```
{
 "id": "0x3eb09d108d1f61f10860b8bb1b13b5b4abc3f49d",
 "token0": "ETH",
 "token1": "USDT",
 "rug_pull": false,
 "score": 12.34
}
```

#### Predict Rug-pull using 7D method

**Endpoint:** /api/predict/7D
**Method**: GET

**Query Parameters:**

- pair_id: The ID of the Uniswap pair to predict.

**Example:**
```
curl -X GET "http://localhost:5000/api/predict/7D?pair_id=0x3eb09d108d1f61f10860b8bb1b13b5b4abc3f49d"
```
Response:
```
{
 "id": "0x3eb09d108d1f61f10860b8bb1b13b5b4abc3f49d",
 "token0": "ETH",
 "token1": "USDT",
 "rug_pull": false,
 "score": 12.34
}
```

