import sqlite3
import pandas as pd

from pathlib import Path

Path('./static/database_objects.db').touch()
conn = sqlite3.connect('./static/database_objects.db')
c = conn.cursor()

c.execute("PRAGMA foreign_keys = ON")

c.execute("DROP TABLE IF EXISTS OBJECTS_HISORICAL_DATA")
c.execute("DROP TABLE IF EXISTS OBJECTS")


#objects table
objects_query = '''
                    CREATE TABLE OBJECTS(
                        objectid int NOT NULL primary key,
                        accessioned int,
                        locationid int,
                        title char(256),
                        displaydate char(256),
                        visualbrowsertimespan char(256),
                        medium char(256),
                        attribution char(1024)

                    )
                '''
c.execute(objects_query)
obj_df = pd.read_csv('objects.csv', usecols=[
    'objectid',
    'accessioned',
    'locationid',
    'title',
    'displaydate',
    'visualbrowsertimespan',
    'medium',
    'attribution'
])
sorted_objects_df = obj_df.sort_values(by=["objectid"], ascending=True)
objects_df = sorted_objects_df.head(40)
objects_df.to_sql('OBJECTS', conn, if_exists='append', index=False)
conn.commit()



# objects historical data table
objects_hist_data_query = '''
                    CREATE TABLE OBJECTS_HISORICAL_DATA(
                        datatype char(32),
                        objectid int,
                        displayorder int(256),
                        forwardtext char(256),
                        invertedtext char(256),
                        remarks char(256),
                        effectivedate char(10),
                        PRIMARY KEY (objectid, displayorder),
                        FOREIGN KEY (objectid) REFERENCES OBJECTS(objectid) ON DELETE CASCADE 
                    )
                '''
c.execute(objects_hist_data_query)
obj_dim_df = pd.read_csv('objects_historical_data.csv', usecols=[
    'datatype',
    'objectid',
    'displayorder',
    'forwardtext',
    'invertedtext',
    'remarks',
    'effectivedate'
])
sorted_objects_dimensions_df = obj_dim_df.sort_values(by=["objectid"], ascending=True)
objects_dimensions_df = sorted_objects_dimensions_df.head(30)
objects_dimensions_df.to_sql('OBJECTS_HISORICAL_DATA', conn, if_exists='append', index=False)
conn.commit()

conn.close()

