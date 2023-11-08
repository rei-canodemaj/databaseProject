

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


