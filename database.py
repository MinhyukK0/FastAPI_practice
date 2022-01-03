import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

user = os.environ['USER']
password = os.environ['PASSWORD']
host = os.environ['HOST']
port = os.environ['PORT']
database = os.environ['PAYHERE_TEST_DB_NAME']

DATABASE_URL = "mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8mb4" % (
    user,
    password,
    host,
    port,
    database,
)

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()