CREATE TABLE IF NOT EXISTS blockchain_table (
    id UUID NOT NULL,
    blockchain VARCHAR(255) NOT NULL,
    sub_chain VARCHAR(255) NOT NULL,
    original BOOL NOT NULL
    start_date DATE NOT NULL,
    description VARCHAR(255) NULL,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id, blockchain, sub_chain)
);

CREATE TABLE IF NOT EXISTS metric_table (
    metric_name VARCHAR(255) PRIMARY KEY,
    display_name VARCHAR(255),
    description TEXT,
    category VARCHAR(255),
    type VARCHAR(255),
    grouping_type VARCHAR(255),
	create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chain_metric (
    blockchain_id UUID NOT NULL,
    blockchain VARCHAR(255) NOT NULL,
    sub_chain VARCHAR(255) NOT NULL,
    metric_name VARCHAR(255),
    FOREIGN KEY (blockchain_id, blockchain, sub_chain) REFERENCES blockchain_table(id, blockchain, sub_chain),
    FOREIGN KEY (metric_name) REFERENCES metric_table(metric_name),
    PRIMARY KEY (blockchain_id, metric_name),
	create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS feature_mappings (
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

CREATE TABLE IF NOT EXISTS metrics_data (
    date DATE NOT NULL,
    blockchain VARCHAR(255) NOT NULL,
    subchain VARCHAR(255) NOT NULL,
    metric VARCHAR(255) NOT NULL,
    value FLOAT NOT NULL
);



DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM metric_table LIMIT 1) THEN
        INSERT INTO metric_table (metric_name, display_name, description, category, type, grouping_type) VALUES
        ('trx_per_second','Transactions Per Second', 'Transactions Per Second (TPS) is a crucial metric that quantifies the blockchain''s throughput, offering a clear view of the average number of transactions processed each second throughout a day. This metric is instrumental in assessing the network''s performance and scalability, with a higher TPS signifying a more robust and efficient blockchain capable of handling increasing transaction demands seamlessly. For businesses and developers evaluating blockchain platforms for high-throughput applications, TPS is a key decision-making factor, reflecting the network''s capacity to support operational requirements without delays. TPS provides a snapshot of network efficiency, positioning itself as an indispensable metric for anyone involved in blockchain development, investment, or analysis, aiming to optimize for speed and reliability.', 'Chain Throughput and Efficiency', 'basic', 'avg'),
        ('trx_per_day','Daily Transactions', 'Transactions Per Day (TPD) encapsulates the total number of transactions processed on the blockchain within a 24-hour timeframe, providing a comprehensive overview of the network''s daily operational activity. This metric is a direct reflection of the blockchain''s vibrancy and user engagement, with higher transaction volumes indicating a lively and participatory network. Conversely, lower transaction volumes may point to reduced usage or interest. For network operators and investors, TPD is an invaluable metric that influences decisions regarding infrastructure investments and market strategy. A consistent uptick in daily transactions signals increasing demand and the potential need for network enhancements to sustain performance levels. TPD offers an unobstructed view of the network''s daily rhythm, essential for those tasked with managing or investing in blockchain technologies.', 'Chain Throughput and Efficiency', 'basic', 'sum'),
        ('total_transactions', 'Total Transactions', 'Total Transactions is a comprehensive metric that tallies the cumulative number of transactions within a specific blockchain subchain, offering a broad perspective on the blockchain''s transactional volume over time. This metric, calculated by simply counting every transaction recorded in the subchain, serves as a crucial indicator of the blockchain''s vibrancy and growth. A high transaction count typically reflects a dynamic and actively used blockchain, showcasing user engagement and network utility. It''s invaluable for blockchain analysts and strategists, enabling them to compare activity levels across different periods, identify trends, and pinpoint potential areas for expansion. Total Transactions provides a macroscopic overview of the blockchain''s development and adoption scale, highlighting its ongoing journey.', 'Network Health and Activity', 'basic', 'sum'),
        ('average_transaction_amount', 'Average Transaction Amount', 'The Average Transaction Amount metric calculates the mean value of transactions within a blockchain subchain for a given day, providing an average that represents the typical transaction size. By dividing the total transaction value by the number of transactions on a specified date, it offers insights into the economic engagement on the blockchain. This metric is instrumental for financial strategists and analysts, helping to understand the market''s direction and the behavior of its participants. A rising Average Transaction Amount may indicate growing confidence and larger capital movements within the network, essential for guiding investment strategies and policy development. It provides a nuanced perspective on the economic interactions within the blockchain, crucial for analyzing financial flows and market dynamics.', 'Economic Indicators', 'basic', 'avg'),
        ('avg_trxs_per_hour', 'Average Transactions Per Hour', 'Transactions Per Hour (TPH) breaks down the daily transaction volume into an hourly average, offering insights into the distribution of transaction activity throughout the day. This metric is vital for understanding the network''s operational efficiency and its consistency in handling transactions over time. For network administrators and developers, TPH is particularly beneficial in identifying peak transaction periods, enabling strategic planning for load management to ensure the network''s performance remains optimal during high-demand intervals. It serves as a lens through which the transactional landscape of the network is examined, playing a critical role in maintaining a responsive and high-performing blockchain ecosystem.', 'Chain Throughput and Efficiency', 'basic', 'avg'),
        ('total_blocks', 'Total Blocks', 'Total Blocks is a fundamental metric reflecting the total number of unique blocks mined in a blockchain subchain, serving as a direct indicator of blockchain activity and scale. It quantifies the operational extent by counting distinct block hashes, offering insights into the blockchain''s growth pace. This metric is pivotal for evaluating the network''s health, security mechanisms (such as proof-of-work or proof-of-stake), and capacity. For developers, investors, and analysts, Total Blocks is crucial for assessing network security, scalability, and efficiency, making it an essential measure of blockchain vitality and operational dynamics.', 'Network Health and Activity', 'basic', 'sum'),
        ('trx_per_block', 'Average Transactions Per Block', 'Transactions Per Block measure the average number of transactions processed within each block, providing a clear view of how transaction loads are managed. By dividing the day''s total transactions by the number of mined blocks, this metric evaluates block space efficiency and the network''s capacity to handle transaction volumes. A higher Transactions Per Block indicates a network optimized for high transaction throughput, essential for scalability and user experience. It aids network planners and architects in determining if adjustments are needed for block size or generation rates, guiding efforts to enhance performance and operational efficiency.', 'Chain Throughput and Efficiency', 'basic', 'avg'),
        ('active_addresses', 'Active Addresses', 'Active Addresses is a pivotal metric that serves as the blockchain''s daily attendance record, revealing the unique addresses that have executed transactions within a single day. By calculating the total count of these addresses, we tap into a direct measure of the network''s daily user engagement and activity levels. This metric not only illuminates the blockchain''s health and adoption rates but also acts as a barometer for its vibrancy. For cryptocurrency traders and market analysts, the Active Addresses trend is a critical indicator, with rising figures suggesting increased user interest and potentially positive market movements, while a decline may hint at falling usage and bearish market sentiments. It embodies the economic pulse of the blockchain, guiding investment decisions and strategic planning with a real-time gauge of network vitality.', 'Network Health and Activity', 'basic', 'sum'),
        ('active_senders', 'Active Senders', 'Active Senders zeroes in on the unique addresses that have initiated transactions, providing an exclusive look at the network''s sending activity. By identifying these addresses, the metric sheds light on the liquidity and active participation within the market. Its significance extends to market analysts and investors who interpret fluctuations in Active Senders as signals of network utility and trading volume changes. A surge in this metric may indicate heightened network engagement or a prelude to increased trading activity, whereas a decrease could reveal a slump in participation, warranting a closer examination of underlying market conditions. Active Senders stands as a beacon, highlighting the transactional momentum and operational dynamics of the blockchain, essential for informed financial and strategic decision-making in the cryptocurrency landscape.', 'Network Health and Activity', 'basic', 'sum'),
        ('sum_emitted_utxo_amount', 'Total Emitted UTXO Value', 'The Sum Emitted UTXO Amount measures the total value of new Unspent Transaction Outputs (UTXOs) generated on a specific day within a blockchain subchain, serving as an indicator of fresh assets being added to the blockchain. This metric quantifies the influx of new assets ready for circulation, calculated by totaling the value of all newly created UTXOs on the chosen date. An increase in the Sum Emitted UTXO Amount suggests vibrant blockchain usage and economic health, marked by a surge in transactions generating new UTXOs. It''s key for blockchain developers and investors to understand the volume of new UTXOs, gauging the liquidity and rate of new asset introduction. A rising SEUA signals a healthy, growing ecosystem, attractive for investment and development, essential for anyone involved in the financial analysis or strategic planning of the blockchain ecosystem.', 'Network Health and Activity', 'basic', 'sum'),
        ('avg_emitted_utxo_amount', 'Average Emitted UTXO Value', 'The Average Emitted UTXO Amount calculates the average value of new UTXOs generated in a blockchain subchain on a chosen day, reflecting the typical size of new assets entering the system. This metric, determined by averaging the value of all newly created UTXOs on the specified date, provides insights into the mean transaction value contributing to new asset circulation. It''s a critical indicator of the economic health and activity within the blockchain, helping stakeholders understand the average value of transactions generating new assets. For investors and blockchain developers, the Average Emitted UTXO Amount is instrumental in assessing the value distribution of new transactions. A higher average suggests larger transactions dominate new asset creation, relevant for asset management strategies and investment decisions. This metric offers a detailed view of the economic activity within the blockchain, crucial for analyzing or influencing the financial landscape.', 'Economic Indicators', 'basic', 'avg'),
        ('median_emitted_utxo_amount', 'Median Emitted UTXO Value', 'The Median Emitted UTXO Amount metric offers a balanced perspective on the value of new assets added to the blockchain, by identifying the central value of all new UTXOs generated on a specific date. This approach minimizes distortion from high-value outliers, providing a grounded view of typical transactional activity. It''s crucial for assessing equitable growth and designing systems that accommodate a wide range of transaction sizes. For blockchain developers and economists, this metric aids in setting benchmarks for transaction fees and policy adjustments, ensuring the blockchain remains accessible and equitable for all users, making it a fundamental tool for understanding the distribution of new asset values.', 'Network Health and Activity', 'basic', 'median'),
        ('sum_consumed_utxo_amount', 'Total Consumed UTXO Value', 'Sum Consumed UTXO Amount reflects the total value of all UTXOs spent or consumed within a blockchain on a given day, highlighting the sum of assets moving within the network. This metric provides a comprehensive view of the day''s economic throughput, indicating active asset transfer and utilization. High values suggest a vibrant, liquid market, essential for blockchain''s economic health. Analysts and strategists rely on this data to gauge spending patterns and liquidity, informing decisions on network scaling, investment, and development of financial products, making it a pivotal indicator of transactional dynamism and economic vitality.', 'Economic Indicators', 'basic', 'sum'),
        ('avg_consumed_utxo_amount', 'Average Consumed UTXO Value', 'The Average Consumed UTXO Amount calculates the mean value of all spent or consumed UTXOs on a specific day, offering insights into the common value of transactions. This metric is key to understanding the average economic activity within the blockchain, indicating the typical size of asset movements. It''s instrumental for economists and developers to assess the network''s efficiency in supporting various transaction sizes and guiding adjustments to maintain accessibility. A higher average signals substantial asset movements, whereas a lower average points to smaller, more frequent transactions, underlining the spending patterns and economic behavior on the blockchain.', 'Economic Indicators', 'basic', 'avg'),
        ('median_consumed_utxo_amount', 'Median Consumed UTXO Value', 'The Median Consumed UTXO Amount provides a genuine reflection of the blockchain''s transactional behavior by identifying the median value of all consumed or spent UTXOs on a chosen day. This metric offers a balanced view of asset transfers, less influenced by outliers than the average. It''s invaluable for creating equitable transaction fee policies and ensuring the blockchain economy remains balanced, accessible to users across transaction sizes. Analysts and policymakers utilize this metric to design systems that foster a healthy, inclusive economic environment, making it essential for understanding standard transaction sizes and promoting equitable growth.', 'Economic Indicators', 'basic', 'median'),
        ('large_trx', 'Large Transactions', 'Large Transaction (LT) quantifies transactions exceeding a preset value threshold, marking those with significant economic impact within the blockchain on a specific day. This metric identifies high-value transactions, offering insights into the network''s capacity to handle substantial economic activities. It''s pivotal for understanding the blockchain''s liquidity and the activity of large stakeholders. For market analysts and investors, LT is crucial for gauging market dynamics and asset distribution shifts, providing a lens into the confidence and actions of major participants. The determination of LT''s threshold, particularly using the third quartile, ensures a meaningful categorization of transactions as ''large,'' highlighting those that are statistically significant within the network''s transactional landscape.', 'Whale Watching', 'basic', 'sum'),
        ('whale_address_activity', 'Whale Address Activity', 'Whale Address Activity (WAA) focuses on transactions that exceed a high-value threshold, indicative of significant movements by large stakeholders, or ''whales,'' within the blockchain. This metric tallies transactions where values surpass a designated benchmark, shedding light on the activities of whales and their impact on the network. High WAA counts can signal pivotal shifts in asset holdings or market positions, potentially presaging broader market movements. For stakeholders, WAA is invaluable for sentiment analysis, risk management, and strategic planning, offering early signals of major economic shifts. The threshold for whale transactions, set at the 96th percentile, balances exclusivity and relevance, effectively capturing the influence of significant market players while maintaining a focused definition of ''whales'' in terms of governance and market impact.', 'Whale Watching', 'basic', 'sum');
    END IF;
END $$;








