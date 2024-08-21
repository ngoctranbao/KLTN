import pandas as pd

# Đọc dữ liệu từ các file CSV
old_pairs = pd.read_csv("./datasets/Pairs.csv")
new_pairs = pd.read_csv("./datasets/etherscan_new_pairs.csv")

# Giả sử cột ID trong cả hai DataFrame là 'id', bạn có thể điều chỉnh nếu cột tên khác
old_ids = set(old_pairs['id'])
new_pairs_filtered = new_pairs[~new_pairs['id'].isin(old_ids)]

# Kết hợp dữ liệu cũ và dữ liệu mới đã được lọc
combined_pairs = pd.concat([old_pairs, new_pairs_filtered])

# Lưu kết quả vào file CSV gốc
combined_pairs.to_csv("./datasets/Pairs.csv", index=False)

# Hiển thị kết quả
print(combined_pairs)