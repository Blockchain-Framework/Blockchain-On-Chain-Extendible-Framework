# workflow_manager.py
import sys
import os
import logging
import argparse
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Ensure the correct paths are included for imports
sys.path.insert(0, 'D:\\Academics\\FYP\\Repos\\Blockchain-On-Chain-Extendible-Framework')

from src.blockchain.avalanche.avalanche_data_extraction import extract_x_chain_data, extract_c_chain_data, extract_p_chain_data
from src.services.data_storage_service import append_dataframe_to_sql, set_last_transaction_data
from src.services.metrics_computation_service import (
    trx_per_second,
    trx_per_day,
    avg_trx_per_block,
    total_trxs,
    total_blocks,
    trx_count,
    cumulative_number_of_trx,
    avg_trx_value,
    median_trx_value,
    avg_utxo_value,
    large_trx,
    whale_address_activity
)


class WorkflowManager:
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.file_path = "file_store"
        self.db_connection_string = os.environ.get("DATABASE_CONNECTION")
        self.functions = {"X": self.run_avalanche_x_data_workflow,
                          "C": self.run_avalanche_c_data_workflow,
                          "P": self.run_avalanche_p_data_workflow,
                          "Bitcoin": self.run_bitcoin_data_workflow}

    def run_avalanche_x_data_workflow(self, start_date):
        try:
            self.logger.info("Extracting Avalanche X data...")
            
            last_date = extract_x_chain_data(start_date)
            
           
            # Store extracted data and update last timestamps
            df_meta_data = pd.DataFrame({
                'timestasmp': [datetime.now()],
                'blockchain':['Avalanche'],
                'sub_chain_name': ['X chain'],
                'note': ['last_date'],
                'value':[last_date]
            })
            df_meta_data['date'] = pd.to_datetime(df_meta_data['date'])
            append_dataframe_to_sql('workflow_meta_table', df_meta_data)

            # Compute metrics
            self.logger.info("Computing metrics...")
            
            self.logger.info("Workflow completed successfully.")
            
        except Exception as e:
            self.logger.error(f"An error occurred during the workflow: {e}")
            
    def run_avalanche_c_data_workflow(self, start_date):
        try:
            self.logger.info("Extracting C Avalanche data...")

            last_date = extract_c_chain_data(start_date)
    
            # Store extracted data and update last timestamps
            df_meta_data = pd.DataFrame({
                'timestasmp': [datetime.now()],
                'blockchain':['Avalanche'],
                'sub_chain_name': ['C chain'],
                'note': ['last_date'],
                'value':[last_date]
            })
            df_meta_data['date'] = pd.to_datetime(df_meta_data['date'])
            append_dataframe_to_sql('workflow_meta_table', df_meta_data)

            # Compute metrics
            self.logger.info("Computing metrics...")
            
            self.logger.info("Workflow completed successfully.")
            
        except Exception as e:
            self.logger.error(f"An error occurred during the workflow: {e}")

    def run_avalanche_p_data_workflow(self, start_date):
        try:
            self.logger.info("Extracting P Avalanche data...")

            last_date = extract_p_chain_data(start_date)

            # Store extracted data and update last timestamps
            df_meta_data = pd.DataFrame({
                'timestasmp': [datetime.now()],
                'blockchain':['Avalanche'],
                'sub_chain_name': ['P chain'],
                'note': ['last_date'],
                'value':[last_date]
            })
            df_meta_data['date'] = pd.to_datetime(df_meta_data['date'])
            append_dataframe_to_sql('workflow_meta_table', df_meta_data)

            # Compute metrics
            self.logger.info("Computing metrics...")
            
            self.logger.info("Workflow completed successfully.")
            
        except Exception as e:
            self.logger.error(f"An error occurred during the workflow: {e}")
            
    def run_bitcoin_data_workflow(self, start_date):
        pass
    
    def run_data_workflow(self):
        # Execute function for all blockchains for 7 days
        current_date = datetime.now()

        # Calculate the date 7 days ago
        date_7_days_ago = current_date - timedelta(days=7)

        # Format the date as a string in "yyyy-mm-dd" format
        start_date = date_7_days_ago.strftime("%Y-%m-%d")
        
        #TODO:  fetch last updatede date from database
        for blockchain in self.functions:
            self.run_data_workflow(start_date, blockchain)
            
    def run_data_workflow(self, start_date, blockchain):
        # Execute function depending on blockchain
        if blockchain in self.functions:
            self.functions[blockchain](start_date)
        else:
            self.logger.error("Unsupported blockchain type")

    def run_data_workflow(self, start_date):
        # Execute workflows for all blockchains
        for blockchain in self.functions:
            self.run_data_workflow(start_date, blockchain)


def caculate_metrics(date_single_day, date_range_full):
    
    # Define date ranges and thresholds for calculations
    # date_single_day = '2024-01-21'
    # date_range_full = ('2024-01-01', '2024-01-21')
    large_trx_threshold = 10000  # Threshold for a large transaction
    whale_trx_threshold = 50000  # Threshold for whale transactions

    
     # Transactions per second
    trx_per_sec = trx_per_second('x_transactions', date_single_day)
    print(f"Transactions per second: {trx_per_sec}")
    df_trx_per_sec = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [trx_per_sec]
    })
    df_trx_per_sec['date'] = pd.to_datetime(df_trx_per_sec['date'])
    append_dataframe_to_sql('trx_per_second', df_trx_per_sec)

    # Transactions per day
    trx_per_day_val = trx_per_day('x_transactions', date_single_day)
    print(f"Transactions per day: {trx_per_day_val}")
    df_trx_per_day = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [trx_per_day_val]
    })
    df_trx_per_day['date'] = pd.to_datetime(df_trx_per_day['date'])
    append_dataframe_to_sql('daily_transaction_count', df_trx_per_day)

    # Average transactions per block
    avg_trx_block = avg_trx_per_block('x_transactions', date_single_day)
    print(f"Average transactions per block: {avg_trx_block}")
    df_avg_trx_block = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [avg_trx_block]
    })
    df_avg_trx_block['date'] = pd.to_datetime(df_avg_trx_block['date'])
    append_dataframe_to_sql('average_transactions_per_block', df_avg_trx_block)

    # Total transactions
    total_transactions = total_trxs('x_transactions')
    print(f"Total transactions: {total_transactions}")
    df_total_transactions = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [total_transactions]
    })
    df_total_transactions['date'] = pd.to_datetime(df_total_transactions['date'])
    append_dataframe_to_sql('total_transactions', df_total_transactions)

    # Total blocks
    total_blocks_val = total_blocks('x_transactions')
    print(f"Total blocks: {total_blocks_val}")
    df_total_blocks = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [total_blocks_val]
    })
    df_total_blocks['date'] = pd.to_datetime(df_total_blocks['date'])
    append_dataframe_to_sql('total_blocks', df_total_blocks)

    # Number of transactions in a specific date range
    trx_count_val = trx_count('x_transactions', date_range_full)
    print(f"Number of transactions in date range {date_range_full}: {trx_count_val}")
    df_trx_count = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [trx_count_val]
    })
    df_trx_count['date'] = pd.to_datetime(df_trx_count['date'])
    append_dataframe_to_sql('number_of_transactions_date_range', df_trx_count)

    # Cumulative number of transactions up to a specified date
    cumulative_trx_val = cumulative_number_of_trx('x_transactions', date_single_day)
    print(f"Cumulative number of transactions up to {date_single_day}: {cumulative_trx_val}")
    df_cumulative_trx = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [cumulative_trx_val]
    })
    df_cumulative_trx['date'] = pd.to_datetime(df_cumulative_trx['date'])
    append_dataframe_to_sql('cumulative_transactions', df_cumulative_trx)

    # Average transaction value in a specific date range
    avg_trx_value_val = avg_trx_value('x_transactions', date_range_full)
    print(f"Average transaction value in date range {date_range_full}: {avg_trx_value_val}")
    df_avg_trx_value = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [avg_trx_value_val]
    })
    df_avg_trx_value['date'] = pd.to_datetime(df_avg_trx_value['date'])
    append_dataframe_to_sql('average_transaction_value', df_avg_trx_value)

    # Median transaction value in a specific date range
    median_trx_value_val = median_trx_value('x_transactions', date_range_full)
    print(f"Median transaction value in date range {date_range_full}: {median_trx_value_val}")
    df_median_trx_value = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [median_trx_value_val]
    })
    df_median_trx_value['date'] = pd.to_datetime(df_median_trx_value['date'])
    append_dataframe_to_sql('median_transaction_value', df_median_trx_value)

    # Average UTXO Value (X-Chain)
    avg_utxo_val_x = avg_utxo_value('x_emitted_utxos', date_range_full)
    print(f"Average UTXO value in X-Chain date range {date_range_full}: {avg_utxo_val_x}")
    df_avg_utxo_value = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [avg_utxo_val_x]
    })
    df_avg_utxo_value['date'] = pd.to_datetime(df_avg_utxo_value['date'])
    append_dataframe_to_sql('average_utxo_value', df_avg_utxo_value)

    # Large Transactions (X-Chain)
    large_trx_val_x = large_trx('x_transactions', date_range_full, large_trx_threshold)
    print(f"Number of large transactions in X-Chain (threshold: {large_trx_threshold}) in date range {date_range_full}: {large_trx_val_x}")
    df_large_transactions = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [large_trx_val_x]
    })
    df_large_transactions['date'] = pd.to_datetime(df_large_transactions['date'])
    append_dataframe_to_sql('large_transactions', df_large_transactions)

    # Whale Address Activity (X-Chain)
    whale_activity_val_x = whale_address_activity('x_transactions', date_range_full, whale_trx_threshold)
    print(f"Number of whale transactions in X-Chain (threshold: {whale_trx_threshold}) in date range {date_range_full}: {whale_activity_val_x}")
    df_whale_activity = pd.DataFrame({
        'date': [date_single_day],
        'blockchain': ['Avalanche'],
        'subchain':['X_chain'],
        'value': [whale_activity_val_x]
    })
    df_whale_activity['date'] = pd.to_datetime(df_whale_activity['date'])
    append_dataframe_to_sql('whale_address_activity', df_whale_activity)

    
def parse_arguments():
    parser = argparse.ArgumentParser(description='Run blockchain data workflow.')

    # Optional argument for start date, defaults to 7 days ago
    parser.add_argument('-d', '--date', type=str, help='Start date in yyyy-mm-dd format', default=(datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"))

    # Required argument for the blockchain type
    parser.add_argument('blockchain', choices=['X', 'C', 'P', 'Bitcoin', 'All'], help='Blockchain type to process (X, C, P, Bitcoin, All)')

    return parser.parse_args()

if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO)
    # args = parse_arguments()

    # manager = WorkflowManager()
    # start_date = args.date

    # if args.blockchain == 'All':
    #     manager.run_data_workflow_for_all(start_date)
    # else:
    #     if args.blockchain in manager.functions:
    #         manager.functions[args.blockchain](start_date)
    #     else:
    #         print(f"Unsupported blockchain type: {args.blockchain}")
    dates = ["2024-01-19","2024-01-20","2024-01-21","2024-01-22","2024-01-23","2024-01-24","2024-01-25","2024-01-26"]
    
    for i in dates:
        caculate_metrics(i, ('2024-01-19', '2024-01-26'))