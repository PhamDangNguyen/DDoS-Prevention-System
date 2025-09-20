from typing import Any, Tuple, Union, Sequence
import pandas as pd
from sklearn.preprocessing import StandardScaler


def _is_hf_dataset(obj: Any) -> bool:
    """Duck-type check for a Hugging Face datasets.Dataset."""
    return hasattr(obj, "to_pandas") and hasattr(obj, "column_names")


def _is_hf_dataset_dict(obj: Any) -> bool:
    """Best-effort check for datasets.DatasetDict without importing datasets."""
    return hasattr(obj, "keys") and hasattr(obj, "__getitem__") and not isinstance(obj, pd.DataFrame)


def _ensure_pandas(x: Any) -> pd.DataFrame:
    """
    Convert supported inputs (HF Dataset/DataFrame) to pandas.DataFrame.
    If a DatasetDict is passed, ask caller to select a split first (e.g., x['train']).
    """
    if _is_hf_dataset_dict(x):
        raise TypeError("Received a DatasetDict. Please select a split first, e.g., ds = ds_dict['train'].")
    if _is_hf_dataset(x):
        return x.to_pandas()
    if isinstance(x, pd.DataFrame):
        return x
    raise TypeError(f"Unsupported data type: {type(x)}. Expected HF Dataset or pandas DataFrame.")


class Preprocessor:
    def __init__(self, name_data: str):
        self.name_data = name_data

    def norm_name_columns(self, data: Union[pd.DataFrame, Any]) -> Union[pd.DataFrame, Any]:
        """
        Normalize column names by stripping leading/trailing whitespace.
        - pandas.DataFrame: returns a new DataFrame with renamed columns.
        - HF datasets.Dataset: returns a new Dataset with renamed columns.
        """
        if _is_hf_dataset(data):
            rename_map = {col: col.strip() for col in data.column_names}
            rename_map = {k: v for k, v in rename_map.items() if k != v}
            return data.rename_columns(rename_map) if rename_map else data

        df = _ensure_pandas(data).copy()
        return df.rename(columns={c: c.strip() for c in df.columns})

    def mapping_label(self, data: Union[pd.DataFrame, Any]) -> pd.DataFrame:
        """
        Map original labels to {DDoS, Normal, Unauthorized Access} for CIC-IDS2017.
        Returns a pandas DataFrame with an extra column `label_mapped`.
        """
        df = _ensure_pandas(data).copy()

        if self.name_data != "CIC-IDS2017":
            return df

        # Robust mapping for common CIC-IDS2017 label variants
        label_category_mapping = {
            'BENIGN': 'Normal',
            'DoS Hulk': 'DDoS',
            'DoS GoldenEye': 'DDoS',
            'DoS slowloris': 'DDoS',
            'DoS Slowhttptest': 'DDoS',
            'DDoS': 'DDoS',
            'PortScan': 'Unauthorized Access', # Mapping PortScan to Unauthorized Access as it can be a prelude to unauthorized access
            'FTP-Patator': 'Unauthorized Access', # Mapping Brute Force to Unauthorized Access
            'SSH-Patator': 'Unauthorized Access', # Mapping Brute Force to Unauthorized Access
            'Web Attack � Brute Force': 'Unauthorized Access', # Mapping Web Attacks to Unauthorized Access
            'Web Attack � XSS': 'Unauthorized Access',
            'Web Attack � Sql Injection': 'Unauthorized Access',
            'Infiltration': 'Unauthorized Access',
            'Bot': 'Unauthorized Access', # Mapping Botnet activities to Unauthorized Access
            'Heartbleed': 'Unauthorized Access' # Mapping Exploits to Unauthorized Access
        }

        # Prefer 'Label' after normalization, but gracefully handle ' Label'
        label_col = None
        if "Label" in df.columns:
            label_col = "Label"
        elif " Label" in df.columns:
            label_col = " Label"
        else:
            raise KeyError("Could not find label column. Expected 'Label' (or original ' Label').")

        # Normalize label text slightly to reduce mismatches
        def _normalize_label_text(x: Any) -> str:
            s = str(x).strip()
            # unify various dash characters to '-'
            s = s.replace("\u2013", "-").replace("\u2014", "-")
            # common capitalization fix
            s = s.replace("Sql Injection", "SQL Injection")
            return s

        df["label_mapped"] = df[label_col].map(lambda x: label_category_mapping.get(_normalize_label_text(x), "Other"))

        # Optional: warn on unknown labels to help debugging
        known_keys = {_normalize_label_text(k) for k in label_category_mapping.keys()}
        unknown = sorted(
            {_normalize_label_text(x) for x in df[label_col].unique()} - known_keys
        )
        if unknown:
            print(f"[WARNING] {len(unknown)} labels not in mapping: {unknown}")

        return df

    def select_columns(self, data: Union[pd.DataFrame, Any], selected_columns: Sequence[str]) -> pd.DataFrame:
        """
        Return a DataFrame containing only the requested columns that exist.
        Prints a warning listing any missing columns.
        """
        df = _ensure_pandas(data).copy()
        missing = [c for c in selected_columns if c not in df.columns]
        if missing:
            print(f"[WARNING] Missing {len(missing)} columns: {missing}")
        else:
            print("All columns in selected_columns are present in the dataset.")
        present = [c for c in selected_columns if c in df.columns]
        return df[present].copy()

    def scale_numerical_features(
        self, df: pd.DataFrame, importance_columns: Sequence[str]
    ) -> Tuple[pd.DataFrame, StandardScaler]:
        """Scale the provided numeric columns using StandardScaler."""
        scaler = StandardScaler()
        cols = [c for c in importance_columns if c in df.columns]
        if cols:
            df = df.copy()
            df[cols] = scaler.fit_transform(df[cols])
        else:
            print("[INFO] No matching columns to scale.")
        return df, scaler

    def main_flow(
        self,
        data: Union[pd.DataFrame, Any],
        selected_columns: Sequence[str],
        importance_columns: Sequence[str],
    ) -> Tuple[pd.DataFrame, StandardScaler]:
        """
        Convenience flow: normalize names -> map labels -> select columns -> scale.
        Accepts either pandas DataFrame or HF Dataset for `data`.
        """
        data = self.norm_name_columns(data)
        df = self.mapping_label(data)
        df = self.select_columns(df, selected_columns)
        df, scaler = self.scale_numerical_features(df, importance_columns)
        return df, scaler

