import pymysql
from sqlalchemy import create_engine

def getConnect():
    db_connection_str = 'mysql+pymysql://bigdata:bigdata@localhost:3306/test'
    db_connection = create_engine(db_connection_str)
    
    return db_connection
 
