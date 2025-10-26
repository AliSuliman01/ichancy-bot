import os
from dotenv import load_dotenv
load_dotenv()

host = os.getenv("DB_HOST")
port =  os.getenv("DB_PORT")
username =  os.getenv("DB_USERNAME")
password =  os.getenv("DB_PASSWORD")
databaseName =  os.getenv("DB_NAME")