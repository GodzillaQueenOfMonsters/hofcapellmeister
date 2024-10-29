from db_connector import ConnectorMariaDB
import error_classes as ec
import os

date_format = '%d. %b %Y'
event_dir = r'/hcm/events_data/'
pl_tr_dir = r'/hcm/pl_tr_data/'
tr_art_dir = r'/hcm/tr_art_data/'

try:
    hcm_db = ConnectorMariaDB()
except ec.DataBaseError as e:
    print(type(e).__name__, e)
# finally:
#     hcm_db.close_connection()

try:
    for file_name in os.listdir(event_dir):
        file_path = os.path.join(event_dir, file_name)
        hcm_db.add_events_from_csv(file_path, date_format)
    for subdir, folders, files in os.walk(pl_tr_dir):
        for file_name in files:
            file_path = os.path.join(subdir, file_name)
            hcm_db.add_pl_tr_from_csv(file_path)
    for subdir, folders, files in os.walk(tr_art_dir):
        for file_name in files:
            file_path = os.path.join(subdir, file_name)
            hcm_db.add_tr_art_from_csv(file_path)
    # for file_name in os.listdir(tr_art_dir):
    #     file_path = os.path.join(tr_art_dir, file_name)
    #
    #     hcm_db.add_tr_art_from_csv(file_path)
except ec.DataBaseError as e:
    print(type(e).__name__, e)
finally:
    hcm_db.close_connection()
