import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import time

def fetch_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="task"
    )
    query = "SELECT * FROM sales"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def main():
    while True:
        data = fetch_data()
        print(data)
        time.sleep(3600)  # wait for 1 hour

if __name__ == "__main__":
    main()
