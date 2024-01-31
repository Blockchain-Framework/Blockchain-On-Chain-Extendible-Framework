from utils.database_service import append_dataframe_to_sql
import pandas as pd

def log_workflow_status(chain, subchain, status, task, error):
    data = {
        'chain': [chain],
        'subchain': [subchain],
        'status': [status],
        'task': [task],
        'error': [error if error else 'None']
    }
    df = pd.DataFrame(data)
    append_dataframe_to_sql('workflow_meta_table', df)
