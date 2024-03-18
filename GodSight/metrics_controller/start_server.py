import os
import django
from django.core.management import call_command

def start_django_server(config, path):
    # Set environment variables based on the config object
    os.environ["DJANGO_SETTINGS_MODULE"] = path
    os.environ["DB_NAME"] = config.db_name
    os.environ["DB_USER"] = config.db_user
    os.environ["DB_HOST"] = config.db_host
    os.environ["DB_PASSWORD"] = config.db_password
    os.environ["DB_PORT"] = config.db_port
    os.environ["SECRET_KEY"] = 'drf-tutorial-123'
    os.environ["DJANGO_ALLOWED_HOSTS"] = config.api_host
    os.environ["DEBUG"] = "1"
    # Set other environment variables as needed

    django.setup()
    call_command('runserver', f'{config.api_host}:{config.api_port}')
