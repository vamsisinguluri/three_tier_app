import os
import json
import psycopg2
import pandas as pd

class PostgresDatabase:


    def database_check(self, host):
        try:
            print("----------- DATABASE ------------")
            print("HOST : ", host)
            print("POSTGRES_DB : ", os.environ['POSTGRES_DB'])
            print("POSTGRES_USER : ", os.environ['POSTGRES_USER'])
            print("POSTGRES_PASSWORD : ", os.environ['POSTGRES_PASSWORD'])
            conn = psycopg2.connect(host=host,
                                    database=os.environ['POSTGRES_DB'],
                                    user=os.environ['POSTGRES_USER'],
                                    password=os.environ['POSTGRES_PASSWORD'])
            return conn
        except Exception as e:
            return None

    def get_db_connection(self):
        phost = os.environ['POSTGRES_PRIMARY_HOST']
        shost = os.environ['POSTGRES_SECONDARY_HOST']
        connection = self.database_check(phost)
        if not connection:
            connection = self.database_check(shost)
            return connection, "SECONDARY"
        return connection, "PRIMARY"

    def insert_userdata(self):
        # parse excel file
        file_path = os.path.dirname(os.path.realpath(__file__)) + os.sep + "user-data.xlsx"
        print("file_path >>>>>>>>", file_path)
        df = pd.read_excel(file_path, parse_dates=['date'], engine='openpyxl')
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        records = json.loads(df.to_json(orient='records'))
        # insert records into database
        conn , app = self.get_db_connection()
        if not conn:
            raise Exception("DB Connection failed.")
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS users;')
        cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                    'name varchar (100) NOT NULL,'
                    'street varchar (150) NOT NULL,'
                    'city varchar (150) NOT NULL,'
                    'state varchar (150) NOT NULL,'
                    'review text,'
                    'date date DEFAULT CURRENT_TIMESTAMP);'
                    )
        for data in records:
            insert_query = "INSERT INTO USERS (name, street, city, state, date) VALUES ('{}', '{}','{}','{}','{}')".format(
                data['name'], data['street'],data['city'],data['state'],data['date'])
            cur.execute(insert_query)
        conn.commit()
        cur.close()
        conn.close()
        return app

    def insert_records(self):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute('DROP TABLE IF EXISTS books;')
        cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                    'title varchar (150) NOT NULL,'
                    'author varchar (50) NOT NULL,'
                    'pages_num integer NOT NULL,'
                    'review text,'
                    'date_added date DEFAULT CURRENT_TIMESTAMP);'
                    )
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    ('A Tale of Two Cities',
                     'Charles Dickens',
                     489,
                     'A great classic!')
                    )
        cur.execute('INSERT INTO books (title, author, pages_num, review)'
                    'VALUES (%s, %s, %s, %s)',
                    ('Anna Karenina',
                     'Leo Tolstoy',
                     864,
                     'Another great classic!')
                    )
        conn.commit()
        cur.close()
        conn.close()





