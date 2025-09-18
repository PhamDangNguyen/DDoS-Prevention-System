from typing import Dict, List, Optional
from datasets import Dataset
from imblearn.over_sampling import SMOTE
import numpy as np
import tqdm

def balance_cicids2017_with_smote(
    ds_train,
    importance_columns: List[str],
    *,
    majority_class_name: str = "Normal",
    majority_original_label: str = "BENIGN",
    oversample_margin: int = 50_000,
    random_state: int = 42,
    smote_neighbors: int = 5,
    label_category_mapping: Optional[Dict[str, str]] = None,
    verbose: bool = True,
):
    """
    Balance CIC-IDS2017 training data using undersampling for the majority class
    and SMOTE oversampling for minority categories (DDoS, Unauthorized Access).

    Expects the input dataset (HuggingFace `Dataset`) to already have:
      - normalized column names (no leading/trailing spaces)
      - original label column: `Label`
      - mapped category column: `label_mapped` (values like 'Normal', 'DDoS', 'Unauthorized Access')

    Parameters
    - ds_train: HuggingFace Dataset (split) after your preprocessing steps
    - importance_columns: list of feature columns (numeric) to use with SMOTE
    - majority_class_name: category name for the majority class (default 'Normal')
    - majority_original_label: original label string representing Normal (default 'BENIGN')
    - oversample_margin: extra samples added to minority target relative to DDoS count
    - random_state: RNG seed for reproducibility
    - smote_neighbors: base k_neighbors for SMOTE; may be reduced per-category if needed
    - label_category_mapping: optional explicit mapping from original labels to categories
    - verbose: print progress

    Returns
    - balanced_ds: HuggingFace Dataset with balanced classes on `label_mapped`
                   and containing only the intersection of columns across parts,
                   typically `importance_columns` + `label_mapped`.
    """
    # Default mapping if none provided
    if label_category_mapping is None:
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

    colnames = set(ds_train.column_names)
    if 'Label' not in colnames:
        raise ValueError("Expected original label column 'Label' to be present in the dataset.")
    if 'label_mapped' not in colnames:
        # Fall back to deriving 'label_mapped' if missing, using provided mapping
        def map_label(example):
            lab = example['Label']
            return {'label_mapped': label_category_mapping.get(lab, 'Other')}

        ds_train = ds_train.map(map_label)
        colnames = set(ds_train.column_names)

    # Count by mapped category
    categorized_counts: Dict[str, int] = {}
    for cat in ds_train['label_mapped']:
        categorized_counts[cat] = categorized_counts.get(cat, 0) + 1

    if verbose:
        print("Category counts (before balancing):", categorized_counts)

    # Determine majority (Normal) subset and target size
    majority_class_dataset = ds_train.filter(
        lambda ex: ex.get('label_mapped', '') == majority_class_name
        or (ex.get('Label', '').strip() == majority_original_label)
    )

    ddos_count = categorized_counts.get('DDoS', 0)
    target_majority_count = ddos_count + int(oversample_margin)

    # Ensure we don't request more than available when undersampling
    majority_n = len(majority_class_dataset)
    target_majority_count = min(target_majority_count, majority_n)

    undersampled_majority_dataset = (
        majority_class_dataset.shuffle(seed=random_state).select(range(target_majority_count))
        if target_majority_count > 0
        else majority_class_dataset
    )

    if verbose:
        print(f"Undersampled '{majority_class_name}' count: {len(undersampled_majority_dataset)}")

    # Prepare minority categories (exclude majority)
    # Group datasets by mapped category, then within each, keep per-original-label splits
    # to allow SMOTE to balance among original labels per category.
    # Build unique original labels present
    unique_labels = set([lbl.strip() for lbl in ds_train['Label']])
    categorized_minority_datasets: Dict[str, List] = {}

    for original_label in unique_labels:
        category = label_category_mapping.get(original_label)
        if category and category != majority_class_name:
            if category not in categorized_minority_datasets:
                categorized_minority_datasets[category] = []
            # Filter rows for this original label
            original_label_ds = ds_train.filter(lambda ex, lab=original_label: ex['Label'].strip() == lab)
            if len(original_label_ds) > 0:
                categorized_minority_datasets[category].append(original_label_ds)
    """
    categorized_minority_datasets structure
    {
    "DDoS": [Dataset("DoS Hulk"), Dataset("DoS GoldenEye"), Dataset("DoS Slowloris"), ...],
    "Unauthorized Access": [Dataset("PortScan"), Dataset("FTP-Patator"), ...]
    }
    """


    # Oversample each minority category using SMOTE on numeric features
    final_oversampled_minority_datasets: List[Dataset] = []

    if verbose:
        print("\nApplying SMOTE to balance minority categories...")

    n_minority_cats = len(categorized_minority_datasets)
    category_target_base = target_majority_count // n_minority_cats if n_minority_cats else 0

    for category, list_of_datasets in tqdm.tqdm(categorized_minority_datasets.items(), desc="Categories"):
        if not list_of_datasets:
            if verbose:
                print(f"  No samples found in category {category}. Skipping SMOTE.")
            continue

        # Concatenate datasets within the same category
        base_cols = list_of_datasets[0].column_names
        combined_dict = {col: [] for col in base_cols}
        for ds_item in list_of_datasets:
            for col in base_cols:
                combined_dict[col].extend(ds_item[col])
        combined_category_ds = Dataset.from_dict(combined_dict)

        if len(combined_category_ds) == 0:
            if verbose:
                print(f"  No samples after combine for {category}. Skipping.")
            continue

        # Extract features and original labels for SMOTE
        # Ensure all importance columns exist
        missing_cols = [c for c in importance_columns if c not in combined_category_ds.column_names]
        if missing_cols:
            raise ValueError(f"Missing required feature columns for SMOTE: {missing_cols}")

        X_category = np.array([combined_category_ds[col] for col in importance_columns]).T
        y_category_original_labels = np.array([lbl.strip() for lbl in combined_category_ds['Label']])

        # Map labels to integers for SMOTE
        unique_original_minority_labels = np.unique(y_category_original_labels)
        if unique_original_minority_labels.size < 2:
            # Only one label in this category; cannot apply SMOTE
            if verbose:
                print(f"  Only one original label in {category}. Keeping originals.")
            keep_dict = {col: combined_category_ds[col] for col in importance_columns}
            keep_dict['label_mapped'] = [category] * len(combined_category_ds)
            final_oversampled_minority_datasets.append(Dataset.from_dict(keep_dict))
            continue

        label_to_int = {label: i for i, label in enumerate(unique_original_minority_labels)}
        int_to_label = {i: label for label, i in label_to_int.items()}
        y_category_int = np.array([label_to_int[label] for label in y_category_original_labels])

        # Determine per-category target
        category_target_count = max(category_target_base, len(combined_category_ds))

        # Current counts per original label within the category
        current_counts: Dict[str, int] = {label: int(np.sum(y_category_original_labels == label))
                                          for label in unique_original_minority_labels}
        total_current = sum(current_counts.values())

        # Build target counts for SMOTE per int label
        original_label_target_counts_in_category: Dict[int, int] = {}
        for orig_label, count in current_counts.items():
            if total_current > 0:
                proportion = count / total_current
                desired = int(category_target_count * proportion)
                target = max(count, desired)
            else:
                target = count
            original_label_target_counts_in_category[label_to_int[orig_label]] = max(target, count)
            """
            original_label_target_counts_in_category = {
                0: 200,   # DoS Hulk
                1: 60,    # DoS Slowloris
                2: 40     # DoS GoldenEye
                }
            """

        # Adjust k_neighbors if any class is too small
        min_class_size = min(current_counts.values()) if current_counts else 0
        if min_class_size <= 1:
            if verbose:
                print(f"  Category {category}: a class has <=1 sample; skipping SMOTE.")
            keep_dict = {col: combined_category_ds[col] for col in importance_columns}
            keep_dict['label_mapped'] = [category] * len(combined_category_ds)
            final_oversampled_minority_datasets.append(Dataset.from_dict(keep_dict))
            continue

        k_neighbors_eff = max(1, min(smote_neighbors, min_class_size - 1))

        if verbose:
            print(f"Processing category: {category}")
            print(f"  Original samples: {len(combined_category_ds)}")
            print(f"  Targets per original label (int): {original_label_target_counts_in_category}")

        try:
            smote = SMOTE(sampling_strategy=original_label_target_counts_in_category,
                          random_state=random_state,
                          k_neighbors=k_neighbors_eff)
            X_resampled, y_resampled_int = smote.fit_resample(X_category, y_category_int)
        except Exception as e:
            # If SMOTE fails, keep original samples for this category
            if verbose:
                print(f"  SMOTE failed for {category} due to: {e}. Keeping originals.")
            keep_dict = {col: combined_category_ds[col] for col in importance_columns}
            keep_dict['label_mapped'] = [category] * len(combined_category_ds)
            final_oversampled_minority_datasets.append(Dataset.from_dict(keep_dict))
            continue

        y_resampled_labels = np.array([int_to_label[i] for i in y_resampled_int])

        if verbose:
            print(f"  Resampled samples: {len(X_resampled)}")

        # Build dataset for this category: keep only features + mapped label
        resampled_dict = {col: X_resampled[:, i].tolist() for i, col in enumerate(importance_columns)}
        resampled_dict['label_mapped'] = [label_category_mapping[label] for label in y_resampled_labels]
        final_oversampled_minority_datasets.append(Dataset.from_dict(resampled_dict))

    # Combine undersampled majority with oversampled minorities
    if final_oversampled_minority_datasets:
        all_parts = [undersampled_majority_dataset] + final_oversampled_minority_datasets
        # Keep only columns present in all parts (usually features + label_mapped)
        common_cols = list(set.intersection(*[set(d.column_names) for d in all_parts]))

        combined: Dict[str, List] = {col: [] for col in common_cols}
        for part in tqdm.tqdm(all_parts, desc="Combining datasets"):  # tqdm to show progress bar in notebookall_parts:
            for col in common_cols:
                combined[col].extend(part[col])

        balanced_ds = Dataset.from_dict(combined)
    else:
        # No minority parts; just use the undersampled majority
        balanced_ds = undersampled_majority_dataset

    if verbose:
        print("\nDataset balancing complete.")
        print(f"Balanced dataset size: {len(balanced_ds)}")
        # Print class distribution by label_mapped
        counts: Dict[str, int] = {}
        for cat in balanced_ds['label_mapped']:
            counts[cat] = counts.get(cat, 0) + 1
        print("Balanced dataset categorized label counts:")
        for cat, cnt in counts.items():
            print(f"  {cat}: {cnt}")

    return balanced_ds
