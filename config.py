import os

from dotenv import load_dotenv

load_dotenv()

SSL_CERT_FILE = os.getenv('SSL_CERT_FILE')
SSL_KEY_FILE = os.getenv('SSL_KEY_FILE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_AUTH_SOURCE = os.getenv('DB_AUTH_SOURCE', 'admin')
TOKEN = os.getenv('TOKEN')
