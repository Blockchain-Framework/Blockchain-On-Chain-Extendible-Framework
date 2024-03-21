from dotenv import load_dotenv
import os


class Config:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env1')
        load_dotenv(dotenv_path=dotenv_path, override=True)
        self.db_host = os.getenv('DB_HOST')
        self.db_name = os.getenv('DB_NAME')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.db_port = os.getenv('DB_PORT')

        self.db_url = os.getenv('DB_URL')

        self.extract_path = os.getenv('EXTRACT_PATH', 'GodSight/data/extract/')
        self.mapper_path = os.getenv('MAPPER_PATH', 'GodSight/data/mappers/')
        self.meta_path = os.getenv('META_PATH', 'GodSight/data/meta/')
        self.metric_path = os.getenv('METRIC_PATH', 'GodSight/data/metric')

        self.extract_exec_path = os.getenv('EXTRACT_EXEC_PATH', 'extraction/')
        self.compute_exec_path = os.getenv('COMPUTE_EXEC_PATH', 'computation/')

        self.api_host = os.getenv('API_HOST', 'localhost')
        self.api_port = os.getenv('API_PORT', '5000')

        self.secret_api_key = os.getenv('SECRET_API_KEY', '123456')

    def __str__(self):
        return (f"Config:\n"
                f"  DB Host: {self.db_host}\n"
                f"  DB Name: {self.db_name}\n"
                f"  DB User: {self.db_user}\n"
                f"  DB Password: {self.db_password}\n"
                f"  DB Password: {'*' * len(self.db_password) if self.db_password else 'Not Set'}\n"
                f"  DB Port: {self.db_port}\n"
                f"  Extract Path: {self.extract_path}\n"
                f"  Mapper Path: {self.mapper_path}\n"
                f"  Meta Path: {self.meta_path}")
