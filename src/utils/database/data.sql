CREATE TABLE IF NOT EXISTS blockchain_table (
    id UUID NOT NULL,
    blockchain VARCHAR(255) NOT NULL,
    sub_chain VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, blockchain, sub_chain)
);

CREATE TABLE IF NOT EXISTS metric_table (
    metric_name VARCHAR(255) PRIMARY KEY,
    description TEXT,
	create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chain_metric (
    blockchain_id UUID NOT NULL,
    blockchain VARCHAR(255) NOT NULL,
    sub_chain VARCHAR(255) NOT NULL,
    metric_name VARCHAR(255),
    category VARCHAR(255),
    FOREIGN KEY (blockchain_id, blockchain, sub_chain) REFERENCES blockchain_table(id, blockchain, sub_chain),
    FOREIGN KEY (metric_name) REFERENCES metric_table(metric_name),
    PRIMARY KEY (blockchain_id, metric_name),
	create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS transactions_feature_mappings (
    id SERIAL,
    blockchain VARCHAR(255) NOT NULL,
	sub_chain VARCHAR(255) NOT NULL,
    sourceField VARCHAR(255) NOT NULL,
    targetField VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'feature' or 'function'
    info VARCHAR(255), -- Function name or NULL
    PRIMARY KEY (id, blockchain, sub_chain, sourceField)
);

CREATE TABLE IF NOT EXISTS emitted_utxos_feature_mappings (
    id SERIAL,
    blockchain VARCHAR(255) NOT NULL,
	sub_chain VARCHAR(255) NOT NULL,
    sourceField VARCHAR(255) NOT NULL,
    targetField VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'feature' or 'function'
    info VARCHAR(255), -- Function name or NULL
    PRIMARY KEY (id, blockchain, sub_chain, sourceField)
);

CREATE TABLE IF NOT EXISTS consumed_utxos_feature_mappings (
    id SERIAL,
    blockchain VARCHAR(255) NOT NULL,
	sub_chain VARCHAR(255) NOT NULL,
    sourceField VARCHAR(255) NOT NULL,
    targetField VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'feature' or 'function'
    info VARCHAR(255), -- Function name or NULL
    PRIMARY KEY (id, blockchain, sub_chain, sourceField)
);






