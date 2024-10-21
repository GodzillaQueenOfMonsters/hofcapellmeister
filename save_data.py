from db_connector import ConnectorMariaDB
from web_logger import return_soup, get_event_data
import error_classes as ec
import sys
import pandas as pd

db_path = 'hofcapellmeister'
user = 'root'
password = ''
host = 'host.docker.internal'
date_format = '%d. %b %Y'


try:
    hcm_db = ConnectorMariaDB(db_name=db_path, user=user, password=password, host=host)
    # print('Database created successfully!')
    # hcm_db.close_connection()
except ec.DataBaseError as e:
    print(type(e).__name__, e)

with open(sys.argv[1], 'r') as input_file:
    artists = input_file.readlines()

for artist in artists:
    artist = artist.strip().replace(' ', '+')
    # create url to search for artist events at volume.at
    a_url = f'https://www.volume.at/?s={artist}&post_type=event'
    # read events info
    try:
        results = get_event_data(return_soup(a_url))
        # save results
        for key, dataframe in results.items():
            try:
                hcm_db.add_events(dataframe)
            except ec.DataBaseError as e:
                print(type(e).__name__, e)
            # finally:
            #     hcm_db.close_connection()
    except KeyError as e:
        print(f"Playlist {artist} could not be read: {e}")
    except TypeError:
        pass