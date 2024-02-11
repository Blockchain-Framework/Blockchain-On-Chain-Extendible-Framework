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
('Avalanche', 'x', '2024-01-19'),
('Avalanche', 'c', '2024-01-19'),
('Avalanche', 'p', '2024-01-19');
('Avalanche', 'default', '2024-01-19');

INSERT INTO metric_table (metric_name, description) VALUES
('trx_per_second', 'Number of transactions processed each second'),
('trx_per_day', 'Total number of transactions processed in a day'),
('total_trxs', 'Cumulative number of transactions processed'),
('total_trx_amount', 'Total amount of transactions'),
('avg_trx_amount', 'Average amount per transaction'),
('trxs_per_hour', 'Average number of transactions processed per hour'),
('total_blocks', 'Total number of blocks in the blockchain'),
('trx_per_block', 'Average number of transactions in each block'),
('active_addresses', 'Number of unique addresses that are active'),
('active_senders', 'Number of unique addresses actively sending transactions'),
('sum_emitted_utxo_amount', 'Total amount of UTXO emitted in transactions'),
('avg_emmited_utxo_amount', 'Average amount of UTXO emitted in transactions'),
('median_emmited_utxo_amount', 'Median amount of UTXO emitted in transactions'),
('sum_consumed_utxo_amount', 'Total amount of UTXO consumed in transactions'),
('avg_consumed_utxo_amount', 'Average amount of UTXO consumed in transactions'),
('median_consumed_utxo_amount', 'Median amount of UTXO consumed in transactions'),
('large_trx', 'Number of transactions exceeding a defined large amount'),
('whale_address_activity', 'Activity level of addresses holding large amounts of currency'),
('total_staked_amount', 'Total amount of currency staked in the network'),
('total_burned_amount', 'Total amount of currency that has been burned or removed from circulation'),
('network_economic_efficiency', 'Evaluates the economic efficiency of transactions over the network'),
('interchain_transactional_coherence', 'Measures the volume and value coherence between different chains or subnets'),
('staking_dynamics_index', 'Analyzes the staking behavior on the network to provide an index of staking attractiveness and profitability'),
('staking_engagement_index','Tracks the level of active engagement in the staking process'),
('interchain_liquidity_ratio', 'Measures the ratio of value transferred between Avalanche chains to the total value created');


INSERT INTO chain_metric (blockchain_id, metric_name, category) VALUES
(1, 'trx_per_second', 'Chain Throughput and Efficiency'),
(1, 'trx_per_day', 'Chain Throughput and Efficiency'),
(1, 'total_trxs', 'Network Health and Activity'),
(1, 'total_trx_amount', 'Economic Indicators'),
(1, 'avg_trx_amount', 'Economic Indicators'),
(1, 'trxs_per_hour', 'Chain Throughput and Efficiency'),
(1, 'total_blocks', 'Network Health and Activity'),
(1, 'trx_per_block', 'Chain Throughput and Efficiency'),
(1, 'active_addresses', 'Network Health and Activity'),
(1, 'active_senders', 'Network Health and Activity'),
(1, 'sum_emitted_utxo_amount', 'Economic Indicators'),
(1, 'avg_emmited_utxo_amount', 'Economic Indicators'),
(1, 'median_emmited_utxo_amount', 'Economic Indicators'),
(1, 'sum_consumed_utxo_amount', 'Economic Indicators'),
(1, 'avg_consumed_utxo_amount', 'Economic Indicators'),
(1, 'median_consumed_utxo_amount', 'Economic Indicators'),
(1, 'large_trx', 'Whale Watching'),
(1, 'whale_address_activity', 'Whale Watching'),
(2, 'trx_per_second', 'Chain Throughput and Efficiency'),
(2, 'trx_per_day', 'Chain Throughput and Efficiency'),
(2, 'total_trxs', 'Network Health and Activity'),
(2, 'total_trx_amount', 'Economic Indicators'),
(2, 'avg_trx_amount', 'Economic Indicators'),
(2, 'trxs_per_hour', 'Chain Throughput and Efficiency'),
(2, 'total_blocks', 'Network Health and Activity'),
(2, 'trx_per_block', 'Chain Throughput and Efficiency'),
(2, 'active_addresses', 'Network Health and Activity'),
(2, 'active_senders', 'Network Health and Activity'),
(2, 'sum_emitted_utxo_amount', 'Economic Indicators'),
(2, 'avg_emmited_utxo_amount', 'Economic Indicators'),
(2, 'median_emmited_utxo_amount', 'Economic Indicators'),
(2, 'sum_consumed_utxo_amount', 'Economic Indicators'),
(2, 'avg_consumed_utxo_amount', 'Economic Indicators'),
(2, 'median_consumed_utxo_amount', 'Economic Indicators'),
(2, 'large_trx', 'Whale Watching'),
(2, 'whale_address_activity', 'Whale Watching'),
(3, 'trx_per_second', 'Chain Throughput and Efficiency'),
(3, 'trx_per_day', 'Chain Throughput and Efficiency'),
(3, 'total_trxs', 'Network Health and Activity'),
(3, 'total_trx_amount', 'Economic Indicators'),
(3, 'avg_trx_amount', 'Economic Indicators'),
(3, 'trxs_per_hour', 'Chain Throughput and Efficiency'),
(3, 'total_blocks', 'Network Health and Activity'),
(3, 'trx_per_block', 'Chain Throughput and Efficiency'),
(3, 'active_addresses', 'Network Health and Activity'),
(3, 'active_senders', 'Network Health and Activity'),
(3, 'sum_emitted_utxo_amount', 'Economic Indicators'),
(3, 'avg_emmited_utxo_amount', 'Economic Indicators'),
(3, 'median_emmited_utxo_amount', 'Economic Indicators'),
(3, 'sum_consumed_utxo_amount', 'Economic Indicators'),
(3, 'avg_consumed_utxo_amount', 'Economic Indicators'),
(3, 'median_consumed_utxo_amount', 'Economic Indicators'),
(3, 'large_trx', 'Whale Watching'),
(3, 'whale_address_activity', 'Whale Watching'),
(3, 'total_staked_amount', 'Economic Indicators'),
(3, 'total_burned_amount', 'Economic Indicators'),
(1, 'network_economic_efficiency', 'Economic Indicators'),
(2, 'network_economic_efficiency', 'Economic Indicators'),
(2, 'interchain_transactional_coherence', 'Chain Throughput and Efficiency'),
(3, 'staking_dynamics_index', 'Network Health and Activity'),
(3, 'staking_engagement_index', 'Network Health and Activity'),
(2, 'interchain_liquidity_ratio', 'Chain Throughput and Efficiency');
