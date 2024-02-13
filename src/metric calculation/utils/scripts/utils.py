import sys
import os
sys.path.insert(0, r"D:\Academics\FYP\Repos new\Blockchain-On-Chain-Extendible-Framework\src\metric calculation")

from utils.database.database_service import append_dataframe_to_sql
import pandas as pd
from datetime import datetime

def log_workflow_status(chain, subchain, status, task, error):
    data = {
        'chain': [chain],
        'subchain': [subchain],
        'status': [status],
        'task': [task],
        'error': [error if error else 'None'],
        'timestasmp': [datetime.now()],
    }
    df = pd.DataFrame(data)
    append_dataframe_to_sql('workflow_meta_table', df)
