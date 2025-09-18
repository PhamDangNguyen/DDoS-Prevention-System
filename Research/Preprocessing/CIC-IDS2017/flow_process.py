
from sklearn.preprocessing import StandardScaler
import numpy as np
from functools import partial

class preprocessor:
    def __init__(self, name_data):
        self.name_data = name_data
    def norm_name_columes(self, dataframe):
        """
        Normalize column names by stripping whitespace.
        """
        current_column_names = dataframe.column_names
        stripped_column_names = {col: col.strip() for col in current_column_names}
        dataframe = dataframe.rename_columns(stripped_column_names)
        return dataframe
    def mapping_label(self, dataframe):
        """
        Map attack labels to DDoS, Normal and Unauthorized Access
        """
        if self.name_data == "CIC-IDS2017":
            label_category_mapping = {
                'BENIGN': 'Normal',
                'DoS Hulk': 'DDoS',
                'DoS GoldenEye': 'DDoS',
                'DoS slowloris': 'DDoS',
                'DoS Slowhttptest': 'DDoS',
                'DDoS': 'DDoS',
                'PortScan': 'Unauthorized Access',
                'FTP-Patator': 'Unauthorized Access',
                'SSH-Patator': 'Unauthorized Access',
                'Web Attack � Brute Force': 'Unauthorized Access',
                'Web Attack � XSS': 'Unauthorized Access',
                'Web Attack � Sql Injection': 'Unauthorized Access',
                'Infiltration': 'Unauthorized Access',
                'Bot': 'Unauthorized Access',
                'Heartbleed': 'Unauthorized Access'
            }

            # xử lý tên cột
            label_col = 'Label'
            if ' Label' in dataframe.column_names:   # đổi .columns -> .column_names
                label_col = ' Label'

            # lấy toàn bộ unique labels
            unique_labels = set(dataframe[label_col])
            mapping_keys = set(label_category_mapping.keys())
            unknown_labels = unique_labels - mapping_keys
            if unknown_labels:
                print(f"[WARNING] Found {len(unknown_labels)} labels not in mapping: {unknown_labels}")

            # HuggingFace Dataset không hỗ trợ trực tiếp .map(dict)
            # phải dùng .map(function)
            def map_label(example):
                return {
                    'label_mapped': label_category_mapping.get(example[label_col], 'Other')
                }

            dataframe = dataframe.map(map_label)

        return dataframe
    
    def select_columns(self, dataframe, selected_columns):
        """
        Create a new dataframe containing only the selected columns
        """
        dataset_columns = dataframe.column_names
        missing_columns = [col for col in selected_columns if col not in dataset_columns]

        if not missing_columns:
            print("All columns in selected_columns are present in the dataset.")
        else:
            print(f"[WARNING] The following columns are missing from the dataset: {missing_columns}")

        # chỉ giữ lại các cột tồn tại trong dataset
        existing_columns = [col for col in selected_columns if col in dataset_columns]

        # trả về dataset mới (copy), chỉ chứa cột cần thiết
        return dataframe.select_columns(existing_columns)
    
    def scale_numerical_features(self,dataset, importance_columns):
        """
        Scale numerical features in a HuggingFace Dataset.
        """
        # Lấy toàn bộ dữ liệu dạng numpy
        numerical_data = np.array([dataset[col] for col in importance_columns]).T
        
        # Chuẩn hóa
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(numerical_data)
        
        # Gán ngược lại vào dataset bằng map
        def update_fn(example, idx):
            for i, col in enumerate(importance_columns):
                example[col] = float(scaled_data[idx, i])  # cast về float để tránh lỗi JSON serialization
            return example

        dataset = dataset.map(update_fn, with_indices=True)
        return dataset
        