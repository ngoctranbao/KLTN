import pandas as pd
from libs import data_collector


pairs_data_path = './datasets/filtered_new_pairs.csv'
raw_data_path = './datasets/WOD.csv'
pairs = pd.read_csv(pairs_data_path)
# Khởi tạo một DataFrame rỗng hoặc đọc từ file nếu đã tồn tại
try:
    raw_data_df = pd.read_csv(raw_data_path)
    print("Existing raw data loaded.")
    processed_pair_ids = set(raw_data_df['id'])  # Tạo tập hợp chứa các pair_id đã xử lý
except FileNotFoundError:
    raw_data_df = pd.DataFrame()
    processed_pair_ids = set()
    print("New raw data DataFrame created.")


# Duyệt qua từng cặp và xử lý dữ liệu
for index, pair in pairs.iterrows():
    if pair['id'] in processed_pair_ids:
        print(f"Skipping already processed pair_id: {pair['id']}")
        continue
    
    data = data_collector.pair_data_wod(pair_id=pair['id'], label=pair['label'])
    
    # Thêm dữ liệu mới vào DataFrame
    new_data_df = pd.DataFrame([data])
    raw_data_df = pd.concat([raw_data_df, new_data_df], ignore_index=True)
    
    # Ghi DataFrame vào tệp CSV
    raw_data_df.to_csv(raw_data_path, index=False)
    print(f"Data for pair_id {pair['id']} saved to {raw_data_path}.")