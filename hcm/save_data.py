from hcm.db_connector import ConnectorMariaDB
import hcm.error_classes as ec
import os


def save_event_data(date_format, event_dir):
    try:
        hcm_db = ConnectorMariaDB()
        for file_name in os.listdir(event_dir):
            file_path = os.path.join(event_dir, file_name)
            hcm_db.add_events_from_csv(file_path, date_format)
    except ec.DataBaseError as e:
        print(type(e).__name__, e)
    except FileNotFoundError:
        print(f"No event data found!")
    except NameError:
        pass


def save_playlist_data(pl_tr_dir, tr_art_dir):
    try:
        hcm_db = ConnectorMariaDB()
        if os.path.isdir(pl_tr_dir):
            for subdir, folders, files in os.walk(pl_tr_dir):
                for file_name in files:
                    file_path = os.path.join(subdir, file_name)
                    hcm_db.add_pl_tr_from_csv(file_path)
        else:
            raise FileNotFoundError("Directory 'pl_tr_dir' not found!")
        if os.path.isdir(tr_art_dir):
            for subdir, folders, files in os.walk(tr_art_dir):
                for file_name in files:
                    file_path = os.path.join(subdir, file_name)
                    hcm_db.add_tr_art_from_csv(file_path)
        else:
            raise FileNotFoundError("Directory 'tr_art_dir' not found!")
        # hcm_db.close_connection()
    except ec.DataBaseError as e:
        print(type(e).__name__, e)
    except FileNotFoundError as e:
        print(e)
    except NameError:
        pass
