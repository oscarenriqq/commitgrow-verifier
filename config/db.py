import os
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    return create_engine(f"mysql+pymysql://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:{str(os.getenv('DBPORT'))}/{os.getenv('DBNAME')}")

def get_metadata():
    return MetaData()

def get_conn():
    return get_engine().connect()