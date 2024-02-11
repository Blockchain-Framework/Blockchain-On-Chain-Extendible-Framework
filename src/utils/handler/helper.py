def format_config_for_insertion(config, blockchain_name, subchain_name):

    table_names = {
        'trx_mapping': 'transactions_feature_mappings',
        'emit_utxo_mapping': 'emitted_utxos_feature_mappings',
        'consume_utxo_mapping': 'consumed_utxos_feature_mappings'
    }
    formatted_data = {
        'transactions_feature_mappings': [],
        'emitted_utxos_feature_mappings': [],
        'consumed_utxos_feature_mappings': []
    }

    for mapping_type, mappings in config.items():
        print(1)
        table_name = table_names[f"{mapping_type}"]  # Map config keys to table names
        for source_field, mapping_info in mappings.items():
            target_field, type_, info = mapping_info[0], mapping_info[1], None
            if len(mapping_info) > 2:
                info = mapping_info[2]  # Function name if it's a function mapping
            
            formatted_entry = {
                'blockchain': blockchain_name,
                'subchain': subchain_name,
                'sourceField': source_field,
                'targetField': target_field,
                'type': type_,
                'info': info
            }
            formatted_data[table_name].append(formatted_entry)
    
    return formatted_data
