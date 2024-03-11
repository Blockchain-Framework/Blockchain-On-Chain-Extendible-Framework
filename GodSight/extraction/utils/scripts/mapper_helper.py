import importlib.util
import pandas as pd

def load_config_from_file(file_path):
    spec = importlib.util.spec_from_file_location("module.name", file_path)
    config_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config_module)
    return config_module.config

def insert_feature_mapping_to_df(blockchain, subchain, mapping):
    # Convert the mapping dictionary to a DataFrame
    data = []
    for source_field, mapping_details in mapping.items():
        target_field, type = mapping_details[:2]
        info = mapping_details[2] if len(mapping_details) > 2 else None  # Get the function name if exists
        data.append({
            'blockchain': blockchain,
            'subchain': subchain,
            'source_field': source_field,
            'target_field': target_field,
            'type': type,
            'info': info or None  # Ensure None is used if info is not provided
        })
    df = pd.DataFrame(data)
    return df