import sqlite3
import pandas as pd

from pathlib import Path
Path('./static/database_constituents.db').touch()
conn = sqlite3.connect('./static/database_constituents.db')
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()



c.execute("DROP TABLE IF EXISTS OBJECTS_CONSTITUENTS")
c.execute("DROP TABLE IF EXISTS CONSTITUENTS")
    
    
    
# constituents table
constituents_query = '''
                    CREATE TABLE CONSTITUENTS(
                        constituentid int NOT NULL PRIMARY KEY,
                        forwarddisplayname char(256),
                        lastname char(256),
                        displaydate char(256),
                        beginyear int,
                        endyear int,
                        nationality char(128),
                        constituenttype char(30)
                    )
                '''
c.execute(constituents_query)
const_df = pd.read_csv('constituents.csv', usecols=[
    'constituentid',
    'forwarddisplayname',
    'lastname',
    'displaydate',
    'beginyear',
    'endyear',
    'nationality',
    'constituenttype'
])
sorted_constituents_df = const_df.sort_values(by=["constituentid"], ascending=False)
constituents_df = sorted_constituents_df.head(40)
constituents_df.to_sql('CONSTITUENTS', conn, if_exists='append', index=False)
conn.commit()




# objects_constituents table
objects_constituents_query = '''
                    CREATE TABLE OBJECTS_CONSTITUENTS(
                        objectid int,
                        constituentid int,
                        displayorder int,
                        roletype char(64),
                        role char(64),
                        displaydate char(128),
                        country char(64),
                        zipcode char(16),
                        PRIMARY KEY (objectid, constituentid, displayorder)
                        FOREIGN KEY (constituentid) REFERENCES CONSTITUENTS(constituentid) ON DELETE CASCADE 
                    )
                '''
c.execute(objects_constituents_query)
obj_const_df = pd.read_csv('objects_constituents.csv', usecols=[
    'objectid',
    'constituentid',
    'displayorder',
    'roletype',
    'role',
    'displaydate',
    'country',
    'zipcode'
])
sorted_obj_const_df = obj_const_df.sort_values(by=["constituentid", "objectid"], ascending=False)
objects_constituents_df = sorted_obj_const_df.head(40)
objects_constituents_df.to_sql('OBJECTS_CONSTITUENTS', conn, if_exists='append', index=False)
conn.commit()

conn.close()