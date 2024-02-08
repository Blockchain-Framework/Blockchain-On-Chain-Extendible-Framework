from dotenv import load_dotenv
import os

class Config:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        dotenv_path = os.path.join(base_dir, 'config', '.env')

        load_dotenv(dotenv_path=dotenv_path)

        self.db_host = os.getenv('DB_HOST')
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.extract_path = os.getenv('EXTRACT_PATH')
        self.mapper_path = os.getenv('MAPPER_PATH')
        self.meta_path = os.getenv('META_PATH')
