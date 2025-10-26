import os
from dotenv import load_dotenv
load_dotenv()

host = os.getenv("HOST")
port =  os.getenv("PORT")
username =  os.getenv("USERNAME")
password =  os.getenv("PASSWORD")
databaseName =  os.getenv("DATABASENAME")