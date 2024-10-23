from db_connector import ConnectorMariaDB
import error_classes as ec
import os
import pandas as pd

db_path = 'hofcapellmeister'
staging_db_name = 'hcm_staging;'
user = 'root'
password = ''
host = 'host.docker.internal'
date_format = '%d. %b %Y'
# file_n = 'C:/Users/am-user347/Documents/hofcapellmeister/events_data/events_vergangene_avenged_sevenfold.csv'
event_dir = r'/hcm/events_data/'
pl_tr_dir = r'/hcm/pl_tr_data/'
tr_art_dir = r'/hcm/tr_art_data/'

try:
    hcm_db = ConnectorMariaDB(db_name=db_path, staging_name=staging_db_name, user=user, password=password, host=host)
    # TODO: check if create table is finished before reading files
    # print('Database created successfully!')
    for file_name in os.listdir(event_dir):
        file_path = os.path.join(event_dir, file_name)
        # print(file_path)
        hcm_db.add_events_from_csv(file_path, date_format)
    for file_name in os.listdir(pl_tr_dir):
        file_path = os.path.join(pl_tr_dir, file_name)
        # print(file_path)
        hcm_db.add_pl_tr_from_csv(file_path)
    for file_name in os.listdir(tr_art_dir):
        file_path = os.path.join(tr_art_dir, file_name)
        print(file_path)
        hcm_db.add_tr_art_from_csv(file_path)

    # hcm_db.close_connection()
except ec.DataBaseError as e:
    print(type(e).__name__, e)


# with open(sys.argv[1], 'r') as input_file:
#     artists = input_file.readlines()
#
# for artist in artists:
#     artist = artist.strip().replace(' ', '+')
#     # create url to search for artist events at volume.at
#     a_url = f'https://www.volume.at/?s={artist}&post_type=event'
#     # read events info
#     try:
#         results = get_event_data(return_soup(a_url))
#         # save results
#         for key, dataframe in results.items():
#             try:
#                 hcm_db.add_events(dataframe, date_format)
#             except ec.DataBaseError as e:
#                 print(type(e).__name__, e)
#             # finally:
#             #     hcm_db.close_connection()
#     except KeyError as e:
#         print(f"Playlist {artist} could not be read: {e}")
#     except TypeError:
#         pass