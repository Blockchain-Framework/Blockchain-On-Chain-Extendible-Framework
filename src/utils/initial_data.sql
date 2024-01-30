CREATE TABLE blockchain_table (
    id SERIAL PRIMARY KEY,
    blockchain VARCHAR(255) NOT NULL,
    sub_chain VARCHAR(255),
    start_date DATE NOT NULL,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE metric_table (
    metric_name VARCHAR(255) PRIMARY KEY,
    description TEXT,
	create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chain_metric (
    blockchain_id INT,
    metric_name VARCHAR(255),
    category VARCHAR(255),
    FOREIGN KEY (blockchain_id) REFERENCES blockchain_table(id),
    FOREIGN KEY (metric_name) REFERENCES metric_table(metric_name),
    PRIMARY KEY (blockchain_id, metric_name),
	create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO blockchain_table (blockchain, sub_chain, start_date) VALUES
('Avalanche', 'X', '2024-01-19'),
('Avalanche', 'C', '2024-01-19'),
('Avalanche', 'P', '2024-01-19');

INSERT INTO metric_table (metric_name, description) VALUES
('trx_per_second', 'Transactions processed per second'),
('trx_per_day', 'Total number of transactions processed per day'),
('avg_trx_per_block', 'Average number of transactions per block'),
('total_trxs', 'Total number of transactions'),
('total_blocks', 'Total number of blocks');

INSERT INTO chain_metric (blockchain_id, metric_name, category) VALUES
(1, 'trx_per_second', 'Transaction Metrics'),
(1, 'trx_per_day', 'Transaction Metrics'),
(1, 'avg_trx_per_block', 'Transaction Metrics'),
(1, 'total_trxs', 'Transaction Metrics'),
(1, 'total_blocks', 'Transaction Metrics'),
(2, 'trx_per_second', 'Transaction Metrics'),
(2, 'trx_per_day', 'Transaction Metrics'),
(2, 'avg_trx_per_block', 'Transaction Metrics'),
(2, 'total_trxs', 'Transaction Metrics'),
(2, 'total_blocks', 'Transaction Metrics'),
(3, 'trx_per_second', 'Transaction Metrics'),
(3, 'trx_per_day', 'Transaction Metrics'),
(3, 'avg_trx_per_block', 'Transaction Metrics'),
(3, 'total_trxs', 'Transaction Metrics'),
(3, 'total_blocks', 'Transaction Metrics');

