

import sqlite3
import pandas as pd

from pathlib import Path

Path('./static/database_locations.db').touch()
conn = sqlite3.connect('./static/database_locations.db')
c = conn.cursor()


conn.execute("PRAGMA foreign_keys = ON")

c.execute("DROP TABLE IF EXISTS LOCATIONS_NEW")
c.execute("DROP TABLE IF EXISTS LOCATIONS_RELATIONS")
c.execute("DROP TABLE IF EXISTS PREFERRED_LOCATIONS")
c.execute("DROP TABLE IF EXISTS LOCATIONS")



#locations table
locations_query = '''
                    CREATE TABLE LOCATIONS(
                        locationid int NOT NULL primary key,
                        site char(256),
                        room char(32),
                        publicaccess int,
                        description char(256),
                        unitposition char(1)
                    )
                '''
c.execute(locations_query)
locat_df = pd.read_csv('locations.csv', usecols=[
    'locationid',
    'site',
    'room',
    'publicaccess',
    'description',
    'unitposition'
])
locat_df.to_sql('LOCATIONS', conn, if_exists='append', index=False)
conn.commit()



#preferred locations table
preferred_locations_query = '''
                    CREATE TABLE PREFERRED_LOCATIONS(
                        locationkey char(32) NOT NULL primary key,
                        locationtype char(256),
                        description char(256),
                        ispublicvenue int,
                        mapimageurl char(1024),
                        mapshapetype char(256),
                        partof char(32)
                    )
                '''
c.execute(preferred_locations_query)
pref_locat_df = pd.read_csv('preferred_locations.csv', usecols=[
    'locationkey',
    'locationtype',
    'description',
    'ispublicvenue',
    'mapimageurl',
    'mapshapetype',
    'partof'
])
sorted_pref_locat_df = pref_locat_df.sort_values(by=["locationkey"], ascending=True)
preferred_locations_df = sorted_pref_locat_df.head(45)
preferred_locations_df.to_sql('PREFERRED_LOCATIONS', conn, if_exists='append', index=False)
conn.commit()



#locations relations table
locations_relations_query = '''
                    CREATE TABLE LOCATIONS_RELATIONS(
                        preferredlocationkey char(32) ,
                        tmslocationid int
                    )
                '''
c.execute(locations_relations_query)
locat_relat_df = pd.read_csv('preferred_locations_tms_locations.csv', usecols=[
    'preferredlocationkey',
    'tmslocationid'
])
locat_relat_df.to_sql('LOCATIONS_RELATIONS', conn, if_exists='append', index=False)
conn.commit()



#location joined table
create_table_query = '''
    CREATE TABLE LOCATIONS_NEW (
        locationid INTEGER NOT NULL PRIMARY KEY,
        site CHAR(256),
        room CHAR(32),
        publicaccess INTEGER,
        description CHAR(256),
        unitposition CHAR(1),
        preferredlocationkey CHAR(32),
        FOREIGN KEY (preferredlocationkey) REFERENCES PREFERRED_LOCATIONS(locationkey) ON DELETE CASCADE 
    )
'''
c.execute(create_table_query)
sql_query = '''
                INSERT INTO LOCATIONS_NEW
                SELECT LOCATIONS.*, LOCATIONS_RELATIONS.preferredlocationkey
                FROM LOCATIONS
                JOIN LOCATIONS_RELATIONS WHERE LOCATIONS.locationid = LOCATIONS_RELATIONS.tmslocationid
                ORDER BY LOCATIONS_RELATIONS.preferredlocationkey ASC
                LIMIT 40
            '''
c.execute(sql_query)
conn.commit()

conn.close()


