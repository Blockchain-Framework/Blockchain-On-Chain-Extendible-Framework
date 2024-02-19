CREATE TABLE blockchain_table (
    id UUID NOT NULL,
    blockchain VARCHAR(255) NOT NULL,
    sub_chain VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);

CREATE TABLE metric_table (
    metric_name VARCHAR(255) PRIMARY KEY,
    display_name VARCHAR(255),
    description TEXT,
    category VARCHAR(255),
    type VARCHAR(255),
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE chain_metric (
    blockchain_id UUID,
    metric_name VARCHAR(255),
    FOREIGN KEY (blockchain_id) REFERENCES blockchain_table(id),
    FOREIGN KEY (metric_name) REFERENCES metric_table(metric_name),
    PRIMARY KEY (blockchain_id, metric_name),
	create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM metric_table) THEN
        INSERT INTO metric_table (metric_name, display_name, description, category, type) VALUES
        ('trx_per_second','Transactions Per Second', 'Transactions Per Second (TPS) is a crucial metric that quantifies the blockchain''s throughput, offering a clear view of the average number of transactions processed each second throughout a day. This metric is instrumental in assessing the network''s performance and scalability, with a higher TPS signifying a more robust and efficient blockchain capable of handling increasing transaction demands seamlessly. For businesses and developers evaluating blockchain platforms for high-throughput applications, TPS is a key decision-making factor, reflecting the network''s capacity to support operational requirements without delays. TPS provides a snapshot of network efficiency, positioning itself as an indispensable metric for anyone involved in blockchain development, investment, or analysis, aiming to optimize for speed and reliability.', 'Chain Throughput and Efficiency', 'basic'),
        ('trx_per_day','Daily Transactions', 'Transactions Per Day (TPD) encapsulates the total number of transactions processed on the blockchain within a 24-hour timeframe, providing a comprehensive overview of the network''s daily operational activity. This metric is a direct reflection of the blockchain''s vibrancy and user engagement, with higher transaction volumes indicating a lively and participatory network. Conversely, lower transaction volumes may point to reduced usage or interest. For network operators and investors, TPD is an invaluable metric that influences decisions regarding infrastructure investments and market strategy. A consistent uptick in daily transactions signals increasing demand and the potential need for network enhancements to sustain performance levels. TPD offers an unobstructed view of the network''s daily rhythm, essential for those tasked with managing or investing in blockchain technologies.', 'Chain Throughput and Efficiency', 'basic');
    END IF;
END $$;


DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM metric_table) THEN
        INSERT INTO metric_table (metric_name, display_name, description, category, type) VALUES
        //('total_trxs', 'Total Transactions', 'Total Transactions is a comprehensive metric that tallies the cumulative number of transactions within a specific blockchain subchain, offering a broad perspective on the blockchain''s transactional volume over time. This metric, calculated by simply counting every transaction recorded in the subchain, serves as a crucial indicator of the blockchain''s vibrancy and growth. A high transaction count typically reflects a dynamic and actively used blockchain, showcasing user engagement and network utility. It''s invaluable for blockchain analysts and strategists, enabling them to compare activity levels across different periods, identify trends, and pinpoint potential areas for expansion. Total Transactions provides a macroscopic overview of the blockchain''s development and adoption scale, highlighting its ongoing journey.', 'Network Health and Activity', 'basic'),
        //('avg_trx_amount', 'Average Transaction Amount', 'The Average Transaction Amount metric calculates the mean value of transactions within a blockchain subchain for a given day, providing an average that represents the typical transaction size. By dividing the total transaction value by the number of transactions on a specified date, it offers insights into the economic engagement on the blockchain. This metric is instrumental for financial strategists and analysts, helping to understand the market''s direction and the behavior of its participants. A rising Average Transaction Amount may indicate growing confidence and larger capital movements within the network, essential for guiding investment strategies and policy development. It provides a nuanced perspective on the economic interactions within the blockchain, crucial for analyzing financial flows and market dynamics.', 'Economic Indicators', 'basic'),
        ('avg_trxs_per_hour', 'Average Transactions Per Hour', 'Transactions Per Hour (TPH) breaks down the daily transaction volume into an hourly average, offering insights into the distribution of transaction activity throughout the day. This metric is vital for understanding the network''s operational efficiency and its consistency in handling transactions over time. For network administrators and developers, TPH is particularly beneficial in identifying peak transaction periods, enabling strategic planning for load management to ensure the network''s performance remains optimal during high-demand intervals. It serves as a lens through which the transactional landscape of the network is examined, playing a critical role in maintaining a responsive and high-performing blockchain ecosystem.', 'Chain Throughput and Efficiency', 'basic'),
        ('total_blocks', 'Total Blocks', 'Total Blocks is a fundamental metric reflecting the total number of unique blocks mined in a blockchain subchain, serving as a direct indicator of blockchain activity and scale. It quantifies the operational extent by counting distinct block hashes, offering insights into the blockchain''s growth pace. This metric is pivotal for evaluating the network''s health, security mechanisms (such as proof-of-work or proof-of-stake), and capacity. For developers, investors, and analysts, Total Blocks is crucial for assessing network security, scalability, and efficiency, making it an essential measure of blockchain vitality and operational dynamics.', 'Network Health and Activity', 'basic'),
        ('avg_tx_per_block', 'Average Transactions Per Block', 'Transactions Per Block measure the average number of transactions processed within each block, providing a clear view of how transaction loads are managed. By dividing the day''s total transactions by the number of mined blocks, this metric evaluates block space efficiency and the network''s capacity to handle transaction volumes. A higher Transactions Per Block indicates a network optimized for high transaction throughput, essential for scalability and user experience. It aids network planners and architects in determining if adjustments are needed for block size or generation rates, guiding efforts to enhance performance and operational efficiency.', 'Chain Throughput and Efficiency', 'basic'),
        ('active_addresses', 'Active Addresses', 'Active Addresses is a pivotal metric that serves as the blockchain''s daily attendance record, revealing the unique addresses that have executed transactions within a single day. By calculating the total count of these addresses, we tap into a direct measure of the network''s daily user engagement and activity levels. This metric not only illuminates the blockchain''s health and adoption rates but also acts as a barometer for its vibrancy. For cryptocurrency traders and market analysts, the Active Addresses trend is a critical indicator, with rising figures suggesting increased user interest and potentially positive market movements, while a decline may hint at falling usage and bearish market sentiments. It embodies the economic pulse of the blockchain, guiding investment decisions and strategic planning with a real-time gauge of network vitality.', 'Network Health and Activity', 'basic'),
        ('active_senders', 'Active Senders', 'Active Senders zeroes in on the unique addresses that have initiated transactions, providing an exclusive look at the network''s sending activity. By identifying these addresses, the metric sheds light on the liquidity and active participation within the market. Its significance extends to market analysts and investors who interpret fluctuations in Active Senders as signals of network utility and trading volume changes. A surge in this metric may indicate heightened network engagement or a prelude to increased trading activity, whereas a decrease could reveal a slump in participation, warranting a closer examination of underlying market conditions. Active Senders stands as a beacon, highlighting the transactional momentum and operational dynamics of the blockchain, essential for informed financial and strategic decision-making in the cryptocurrency landscape.', 'Network Health and Activity', 'basic'),
        ('sum_emitted_utxo_amount', 'Total Emitted UTXO Value', 'The Sum Emitted UTXO Amount measures the total value of new Unspent Transaction Outputs (UTXOs) generated on a specific day within a blockchain subchain, serving as an indicator of fresh assets being added to the blockchain. This metric quantifies the influx of new assets ready for circulation, calculated by totaling the value of all newly created UTXOs on the chosen date. An increase in the Sum Emitted UTXO Amount suggests vibrant blockchain usage and economic health, marked by a surge in transactions generating new UTXOs. It''s key for blockchain developers and investors to understand the volume of new UTXOs, gauging the liquidity and rate of new asset introduction. A rising SEUA signals a healthy, growing ecosystem, attractive for investment and development, essential for anyone involved in the financial analysis or strategic planning of the blockchain ecosystem.', 'Network Health and Activity', 'basic'),
        ('avg_emmited_utxo_amount', 'Average Emitted UTXO Value', 'The Average Emitted UTXO Amount calculates the average value of new UTXOs generated in a blockchain subchain on a chosen day, reflecting the typical size of new assets entering the system. This metric, determined by averaging the value of all newly created UTXOs on the specified date, provides insights into the mean transaction value contributing to new asset circulation. It''s a critical indicator of the economic health and activity within the blockchain, helping stakeholders understand the average value of transactions generating new assets. For investors and blockchain developers, the Average Emitted UTXO Amount is instrumental in assessing the value distribution of new transactions. A higher average suggests larger transactions dominate new asset creation, relevant for asset management strategies and investment decisions. This metric offers a detailed view of the economic activity within the blockchain, crucial for analyzing or influencing the financial landscape.', 'Economic Indicators', 'basic'),
        ('median_emmited_utxo_amount', 'Median Emitted UTXO Value', 'The Median Emitted UTXO Amount metric offers a balanced perspective on the value of new assets added to the blockchain, by identifying the central value of all new UTXOs generated on a specific date. This approach minimizes distortion from high-value outliers, providing a grounded view of typical transactional activity. It''s crucial for assessing equitable growth and designing systems that accommodate a wide range of transaction sizes. For blockchain developers and economists, this metric aids in setting benchmarks for transaction fees and policy adjustments, ensuring the blockchain remains accessible and equitable for all users, making it a fundamental tool for understanding the distribution of new asset values.', 'Network Health and Activity', 'basic');
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM metric_table) THEN
        INSERT INTO metric_table (metric_name, display_name, description, category, type) VALUES
     ('sum_consumed_utxo_amount', 'Total Consumed UTXO Value', 'Sum Consumed UTXO Amount reflects the total value of all UTXOs spent or consumed within a blockchain on a given day, highlighting the sum of assets moving within the network. This metric provides a comprehensive view of the day''s economic throughput, indicating active asset transfer and utilization. High values suggest a vibrant, liquid market, essential for blockchain''s economic health. Analysts and strategists rely on this data to gauge spending patterns and liquidity, informing decisions on network scaling, investment, and development of financial products, making it a pivotal indicator of transactional dynamism and economic vitality.', 'Economic Indicators', 'basic'),
        ('avg_consumed_utxo_amount', 'Average Consumed UTXO Value', 'The Average Consumed UTXO Amount calculates the mean value of all spent or consumed UTXOs on a specific day, offering insights into the common value of transactions. This metric is key to understanding the average economic activity within the blockchain, indicating the typical size of asset movements. It''s instrumental for economists and developers to assess the network''s efficiency in supporting various transaction sizes and guiding adjustments to maintain accessibility. A higher average signals substantial asset movements, whereas a lower average points to smaller, more frequent transactions, underlining the spending patterns and economic behavior on the blockchain.', 'Economic Indicators', 'basic'),
        ('median_consumed_utxo_amount', 'Median Consumed UTXO Value', 'The Median Consumed UTXO Amount provides a genuine reflection of the blockchain''s transactional behavior by identifying the median value of all consumed or spent UTXOs on a chosen day. This metric offers a balanced view of asset transfers, less influenced by outliers than the average. It''s invaluable for creating equitable transaction fee policies and ensuring the blockchain economy remains balanced, accessible to users across transaction sizes. Analysts and policymakers utilize this metric to design systems that foster a healthy, inclusive economic environment, making it essential for understanding standard transaction sizes and promoting equitable growth.', 'Economic Indicators', 'basic'),
        ('large_trx', 'Large Transactions', 'Large Transaction (LT) quantifies transactions exceeding a preset value threshold, marking those with significant economic impact within the blockchain on a specific day. This metric identifies high-value transactions, offering insights into the network''s capacity to handle substantial economic activities. It''s pivotal for understanding the blockchain''s liquidity and the activity of large stakeholders. For market analysts and investors, LT is crucial for gauging market dynamics and asset distribution shifts, providing a lens into the confidence and actions of major participants. The determination of LT''s threshold, particularly using the third quartile, ensures a meaningful categorization of transactions as ''large,'' highlighting those that are statistically significant within the network''s transactional landscape.', 'Whale Watching', 'advanced'),
        ('whale_address_activity', 'Whale Address Activity', 'Whale Address Activity (WAA) focuses on transactions that exceed a high-value threshold, indicative of significant movements by large stakeholders, or ''whales,'' within the blockchain. This metric tallies transactions where values surpass a designated benchmark, shedding light on the activities of whales and their impact on the network. High WAA counts can signal pivotal shifts in asset holdings or market positions, potentially presaging broader market movements. For stakeholders, WAA is invaluable for sentiment analysis, risk management, and strategic planning, offering early signals of major economic shifts. The threshold for whale transactions, set at the 96th percentile, balances exclusivity and relevance, effectively capturing the influence of significant market players while maintaining a focused definition of ''whales'' in terms of governance and market impact.', 'Whale Watching', 'advanced'),
        ('total_staked_amount', 'Total Staked Value', 'Total Staked Amount sums up the aggregate of tokens staked on a specific day, highlighting the commitment of participants to the network''s security or investment. This metric is a critical indicator of blockchain health, user trust, and the overall stability of the network. A high total staked amount signals strong network confidence and engagement, essential for security and stability. Network administrators and investors monitor this metric to gauge active engagement and financial backing, with increasing trends suggesting growing network confidence and attracting further participation and investment, thus providing a snapshot of network', 'Economic Indicators', 'basic'),
        ('total_burned_amount', 'Total Burned Value', 'Total Burned Amount quantifies tokens burned or removed from circulation on a specific day, a strategy for supply management and value stimulation. This metric reflects the network''s dedication to controlling token supply, impacting stakeholder confidence and market dynamics. A high burn rate can indicate bullish market strategies, potentially leading to increased token demand and price due to reduced supply. Investors and economic analysts view this as a critical indicator of the network''s long-term value proposition and supply management approach, offering insights into strategic economic decisions and their impact on the blockchain ecosystem.', 'Economic Indicators', 'basic'),
        ('staking_dynamics_index', 'Staking Dynamics Index', 'The Staking Dynamics Index (SDI) encapsulates Avalanche''s staking landscape by evaluating staking attractiveness through rewards, costs, and the overall staking process efficiency. It combines the total staked amount, expected rewards, and delegation fees to gauge staking''s economic dynamics. A high SDI suggests a lucrative staking environment, promoting network participation and security. SDI is critical for validators and potential stakers to assess returns, guiding network administrators in optimizing staking incentives and policies to bolster network health and growth.', 'Economic Indicators', 'advanced'),
        ('staking_engagement_index', 'Staking Engagement Index', 'The Staking Engagement Index (SEI) assesses the reward appeal in Avalanche''s staking mechanism, providing a ratio of estimated rewards to the staked amount. It signifies the reward per unit stake, highlighting the network''s capacity to offer attractive returns to its security participants. A higher SEI indicates a more enticing staking environment, encouraging participation and enhancing network security. SEI serves as a benchmark for evaluating staking returns, aiding stakeholders in making informed decisions on resource allocation and network developers in tailoring staking strategies to improve engagement and security.', 'Economic Indicators', 'advanced'),
        ('interchain_transactional_coherence', 'Interchain Transactional Coherence', 'Interchain Transactional Coherence (ITC) quantifies Avalanche''s efficiency in facilitating cross-chain transactions, marking its interoperability within the blockchain ecosystem. By measuring the value ratio of cross-chain transactions to overall network activity, ITC underscores Avalanche''s integration and fluidity in supporting a multi-chain environment. A high ITC value indicates effective cross-chain transaction integration, crucial for platforms aiming to support diverse blockchain applications. This metric offers insights into Avalanche''s role as an interconnectivity hub, guiding development and strategic decisions to enhance its cross-chain functionalities.', 'Chain Throughput and Efficiency', 'advanced'),
        ('interchain_liquidity_ratio', 'Interchain Liquidity Ratio', 'The Interchain Liquidity Ratio (ILR) evaluates the Avalanche network''s liquidity by comparing asset flows between chains to its internal asset generation. It highlights Avalanche''s role in the crypto ecosystem, demonstrating its interconnectedness and liquidity hub status. A high ILR signifies strong interchain activity, underscoring Avalanche''s appeal for multi-chain applications. This metric is invaluable for strategists and investors assessing Avalanche''s utility, interoperability, and liquidity management, spotlighting its capacity to bridge economic activities across blockchain networks.', 'Economic Indicators', 'advanced'),
        ('network_economy_efficiency', 'Network Economic Efficiency', 'Network Economic Efficiency (NEE) examines the balance between the network''s economic activity and its token deflationary measures by comparing transaction values to tokens burned. A higher NEE indicates an efficient, sustainable economy where transactional value surpasses token burn rates, reflecting a healthy economic model. It provides crucial insights into the network''s economic health, guiding participants and investors in evaluating the network''s sustainability and informing policy development to enhance economic efficiency. NEE is vital for understanding economic activities'' sustainability, ensuring the network''s long-term vibrancy and growth.', 'Economic Indicators', 'advanced');
    END IF;
END $$;


DO $$
BEGIN
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    IF NOT EXISTS (SELECT 1 FROM blockchain_table) THEN
        INSERT INTO blockchain_table (id, blockchain, sub_chain, start_date) VALUES
        (uuid_generate_v4(), 'Avalanche', 'x', '2024-01-19'),
        (uuid_generate_v4(), 'Avalanche', 'c', '2024-01-19'),
        (uuid_generate_v4(), 'Avalanche', 'p', '2024-01-19'),
        (uuid_generate_v4(), 'Avalanche', 'default', '2024-01-19');
    END IF;
END $$;

-- INSERT INTO metric_table (metric_name, description) VALUES
-- ('trx_per_second', 'Number of transactions processed each second'),
-- ('trx_per_day', 'Total number of transactions processed in a day'),
-- ('total_trxs', 'Cumulative number of transactions processed'),
-- ('avg_trx_amount', 'Average amount per transaction'),
-- ('avg_trxs_per_hour', 'Average number of transactions processed per hour'),
-- ('total_blocks', 'Total number of blocks in the blockchain'),
-- ('avg_tx_per_block', 'Average number of transactions in each block'),
-- ('active_addresses', 'Number of unique addresses that are active'),
-- ('active_senders', 'Number of unique addresses actively sending transactions'),
-- ('cumulative_number_of_trx', 'Total number of transactions ever processed'),
-- ('sum_emitted_utxo_amount', 'Total amount of UTXO emitted in transactions'),
-- ('avg_emmited_utxo_amount', 'Average amount of UTXO emitted in transactions'),
-- ('median_emmited_utxo_amount', 'Median amount of UTXO emitted in transactions'),
-- ('sum_consumed_utxo_amount', 'Total amount of UTXO consumed in transactions'),
-- ('avg_consumed_utxo_amount', 'Average amount of UTXO consumed in transactions'),
-- ('median_consumed_utxo_amount', 'Median amount of UTXO consumed in transactions'),
-- ('large_trx', 'Number of transactions exceeding a defined large amount'),
-- ('whale_address_activity', 'Activity level of addresses holding large amounts of currency'),
-- ('total_staked_amount', 'Total amount of currency staked in the network'),
-- ('total_burned_amount', 'Total amount of currency that has been burned or removed from circulation');
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM chain_metric) THEN
    INSERT INTO chain_metric (blockchain_id, metric_name) VALUES
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'trx_per_second'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'trx_per_day'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'total_trxs'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'avg_trx_amount'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'avg_trxs_per_hour'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'total_blocks'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'avg_tx_per_block'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'active_addresses'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'active_senders'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'sum_emitted_utxo_amount'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'avg_emmited_utxo_amount'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'median_emmited_utxo_amount'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'sum_consumed_utxo_amount'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'avg_consumed_utxo_amount'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'median_consumed_utxo_amount'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'large_trx'),
    ('b6aa4213-766f-482d-8d29-8f5c613e3167', 'whale_address_activity'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'trx_per_second'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'trx_per_day'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'total_trxs'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'avg_trx_amount'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'avg_trxs_per_hour'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'total_blocks'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'avg_tx_per_block'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'active_addresses'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'active_senders'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'cumulative_number_of_trx'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'sum_emitted_utxo_amount'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'avg_emmited_utxo_amount'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'median_emmited_utxo_amount'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'sum_consumed_utxo_amount'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'avg_consumed_utxo_amount'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'median_consumed_utxo_amount'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'large_trx'),
    ('3a8855ac-fc5d-4f78-8782-eba2d5175ded', 'whale_address_activity'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'trx_per_second'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'trx_per_day'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'total_trxs'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'avg_trx_amount'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'avg_trxs_per_hour'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'total_blocks'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'avg_tx_per_block'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'active_addresses'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'active_senders'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'cumulative_number_of_trx'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'sum_emitted_utxo_amount'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'avg_emmited_utxo_amount'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'median_emmited_utxo_amount'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'sum_consumed_utxo_amount'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'avg_consumed_utxo_amount'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'median_consumed_utxo_amount'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'large_trx'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'whale_address_activity'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'total_staked_amount'),
    ('37fd6614-b10c-4656-a92b-fe050557b512', 'total_burned_amount'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'trx_per_second'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'trx_per_day'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'total_trxs'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'avg_trx_amount'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'avg_trxs_per_hour'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'total_blocks'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'avg_tx_per_block'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'active_addresses'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'active_senders'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'cumulative_number_of_trx'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'sum_emitted_utxo_amount'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'avg_emmited_utxo_amount'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'median_emmited_utxo_amount'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'sum_consumed_utxo_amount'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'avg_consumed_utxo_amount'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'median_consumed_utxo_amount'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'large_trx'),
    ('eeaa1613-bb74-428c-97da-cac4329c7d7b', 'whale_address_activity');
    END IF;
END $$;

CREATE TABLE transactions_feature_mappings (
    id SERIAL PRIMARY KEY,
    blockchain VARCHAR(255) NOT NULL,
	subchain VARCHAR(255) NOT NULL,
    sourceField VARCHAR(255) NOT NULL,
    targetField VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'feature' or 'function'
    info VARCHAR(255) -- Function name or NULL
);

CREATE TABLE emitted_utxos_feature_mappings (
    id SERIAL PRIMARY KEY,
    blockchain VARCHAR(255) NOT NULL,
	subchain VARCHAR(255) NOT NULL,
    sourceField VARCHAR(255) NOT NULL,
    targetField VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'feature' or 'function'
    info VARCHAR(255) -- Function name or NULL
);

CREATE TABLE consumed_utxos_feature_mappings (
    id SERIAL PRIMARY KEY,
    blockchain VARCHAR(255) NOT NULL,
	subchain VARCHAR(255) NOT NULL,
    sourceField VARCHAR(255) NOT NULL,
    targetField VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'feature' or 'function'
    info VARCHAR(255) -- Function name or NULL
);

INSERT INTO transactions_feature_mappings (blockchain, subchain, sourceField, targetField, type, info) VALUES
('Avalanche', 'x', 'txHash', 'txHash', 'feature', NULL),
('Avalanche', 'x', 'blockHash', 'blockHash', 'feature', NULL),
('Avalanche', 'x', 'blockHeight', 'blockHeight', 'feature', NULL),
('Avalanche', 'x', 'timestamp', 'timestamp', 'feature', NULL),
('Avalanche', 'x', 'memo', 'memo', 'feature', NULL),
('Avalanche', 'x', 'chainFormat', 'chainFormat', 'feature', NULL),
('Avalanche', 'x', 'txType', 'txType', 'feature', NULL),
('Avalanche', 'x', 'amount_unlocked', 'amountUnlocked', 'function', 'calculate_amount_unlocked'),
('Avalanche', 'x', 'amount_created', 'amountCreated', 'function', 'calculate_amount_created');

INSERT INTO emitted_utxos_feature_mappings (blockchain, subchain, sourceField, targetField, type, info) VALUES
('x', 'default', 'addresses', 'addresses', 'feature', NULL),
('x', 'default', 'utxoId', 'utxoId', 'feature', NULL),
('x', 'default', 'txHash', 'txHash', 'feature', NULL),
('x', 'default', 'txType', 'txType', 'feature', NULL),
('x', 'default', 'assetId', 'assetId', 'function', 'getAssetId'),
('x', 'default', 'asset_name', 'assetName', 'function', 'getAssetName'),
('x', 'default', 'symbol', 'symbol', 'function', 'getSymbol'),
('x', 'default', 'denomination', 'denomination', 'function', 'getDenomination'),
('x', 'default', 'asset_type', 'assetType', 'function', 'getAsset_type'),
('x', 'default', 'amount', 'amount', 'function', 'getAmount');

INSERT INTO consumed_utxos_feature_mappings (blockchain, subchain, sourceField, targetField, type, info) VALUES
('x', 'default', 'addresses', 'addresses', 'feature', NULL),
('x', 'default', 'utxoId', 'utxoId', 'feature', NULL),
('x', 'default', 'txHash', 'txHash', 'feature', NULL),
('x', 'default', 'txType', 'txType', 'feature', NULL),
('x', 'default', 'blockHash', 'blockHash', 'feature', NULL),
('x', 'default', 'assetId', 'assetId', 'function', 'getAssetId'),
('x', 'default', 'asset_name', 'assetName', 'function', 'getAssetName'),
('x', 'default', 'symbol', 'symbol', 'function', 'getSymbol'),
('x', 'default', 'denomination', 'denomination', 'function', 'getDenomination'),
('x', 'default', 'asset_type', 'assetType', 'function', 'getAsset_type'),
('x', 'default', 'amount', 'amount', 'function', 'getAmount');
