import mysql.connector
import pandas as pd
import error_classes as ec


class ConnectorMariaDB:
    def __init__(self, db_name, user, password, host):
        self.__db_name = db_name
        try:
            self.__connection = mysql.connector.connect(
                database=self.__db_name,
                host=host,
                user=user,
                password=password,
                allow_local_infile=True
            )
        except Exception as e:
            raise ec.DataBaseError(f"Error while connecting to server. {type(e).__name__}: {e}")
        try:
            self.__create_hcm_tables()
        except ec.DataBaseError as e:
            print(e)

    def __create_hcm_tables(self):
        query_playlist = '''
        CREATE TABLE IF NOT EXISTS playlist (
                pl_id BIGINT PRIMARY KEY,
                pl_name VARCHAR(100) NOT NULL
                );'''
        query_track = '''
        CREATE TABLE IF NOT EXISTS track (
                tr_id BIGINT PRIMARY KEY,
                tr_name VARCHAR(100) NOT NULL
                );'''
        query_artist = '''
            CREATE TABLE IF NOT EXISTS artist (
                art_id BIGINT PRIMARY KEY,
                art_name VARCHAR(100) NOT NULL
                );'''
        query_event = '''
            CREATE TABLE IF NOT EXISTS event (
                ev_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                ev_name VARCHAR(100) NOT NULL,
                ev_date DATE NOT NULL,
                ev_location VARCHAR(100) NOT NULL,
                UNIQUE(ev_name, ev_date, ev_location)
                );'''
        query_art_ev = '''
            CREATE TABLE IF NOT EXISTS art_ev (
                art_id BIGINT,
                ev_id BIGINT,
                search_term VARCHAR(100) NOT NULL,
                PRIMARY KEY(art_id, ev_id),
                FOREIGN KEY(art_id) REFERENCES artist(art_id),
                FOREIGN KEY(ev_id) REFERENCES event(ev_id)
                );'''
        query_art_tr = '''
            CREATE TABLE IF NOT EXISTS art_tr (
                art_id BIGINT,
                tr_id BIGINT,
                PRIMARY KEY(art_id, tr_id),
                FOREIGN KEY(art_id) REFERENCES artist(art_id),
                FOREIGN KEY(tr_id) REFERENCES track(tr_id)
                );'''
        query_pl_tr = '''
            CREATE TABLE IF NOT EXISTS pl_tr (
                pl_id BIGINT,
                tr_id BIGINT,
                PRIMARY KEY(pl_id, tr_id),
                FOREIGN KEY(pl_id) REFERENCES playlist(pl_id),
                FOREIGN KEY(tr_id) REFERENCES track(tr_id)
                );'''
        query_view_event_all_info = '''
            CREATE OR REPLACE VIEW event_all_info AS (
                SELECT ev_name, ev_date, ev_location, search_term, art_name, art_id, pl_name
                FROM
                event JOIN art_ev USING (ev_id)
                JOIN artist USING (art_id)
                JOIN art_tr USING (art_id)
                JOIN pl_tr USING (tr_id)
                JOIN playlist USING (pl_id)
                );'''
        query_view_artist_all_info = '''
            CREATE OR REPLACE VIEW artist_all_info AS (
                SELECT art_id, art_name, tr_name, pl_name
                FROM
                artist JOIN art_tr USING (art_id)
                JOIN track USING (tr_id) 
                JOIN pl_tr USING (tr_id)
                JOIN playlist USING (pl_id)
                );'''

        try:
            cursor = self.__connection.cursor()
            for query in (query_playlist,
                          query_track,
                          query_artist,
                          query_event,
                          query_art_ev,
                          query_art_tr,
                          query_pl_tr,
                          query_view_event_all_info,
                          query_view_artist_all_info):
                cursor.execute(query)
        except Exception as e:
            raise ec.DataBaseError(f"Error while creating hcm tables. {type(e).__name__}: {e}")

    def __dataframe_from_query(self, query, params):
        self.__connection.reconnect()
        cursor = self.__connection.cursor()
        cursor.execute(query, params=params)
        columns = [desc_list[0] for desc_list in cursor.description]
        return pd.DataFrame(cursor.fetchall(), columns=columns)

    def add_events_from_csv(self, file_name, date_format='%d. %b %Y'):
        query_event = '''
        load data local infile %s
        ignore into table event
        CHARACTER SET utf8mb4
        columns terminated by ';'
        ignore 1 lines
        (ev_name, @ev_date, ev_location, @search_term, @art_id)
        set ev_date=(SELECT STR_TO_DATE(@ev_date, %s));'''
        query_art_ev = '''
        load data local infile %s
        ignore into table art_ev
        CHARACTER SET utf8mb4
        columns terminated by ';'
        ignore 1 lines
        (@ev_name, @ev_date, @ev_location, search_term, art_id)
        set ev_id=(SELECT ev_id from event 
        WHERE ev_name = @ev_name AND
        ev_date = STR_TO_DATE(@ev_date, %s) AND
        ev_location = @ev_location);'''
        try:
            self.__connection.reconnect()
            cursor = self.__connection.cursor()
            for query in (query_event, query_art_ev):
                cursor.execute(query, (file_name, date_format))
            self.__connection.commit()
        except Exception as e:
            raise ec.DataBaseError(f"Error while adding events. {type(e).__name__}: {e}")

    def add_pl_tr_from_csv(self, file_name):
        query_pl_tr = '''
        LOAD DATA LOCAL INFILE %s
        IGNORE INTO TABLE pl_tr
        CHARACTER SET utf8mb4
        COLUMNS TERMINATED BY ';'
        IGNORE 1 LINES
        (pl_id, @pl_name, tr_id, @tr_name);'''
        query_track = '''
        LOAD DATA LOCAL INFILE %s
        IGNORE INTO TABLE track
        CHARACTER SET utf8mb4
        COLUMNS TERMINATED BY ';'
        IGNORE 1 LINES
        (@pl_id, @pl_name, tr_id, tr_name);'''
        query_playlist = '''
        LOAD DATA LOCAL INFILE %s
        IGNORE INTO TABLE playlist
        CHARACTER SET utf8mb4
        COLUMNS TERMINATED BY ';'
        IGNORE 1 LINES
        (pl_id, pl_name, @tr_id, @tr_name);'''
        try:
            self.__connection.reconnect()
            cursor = self.__connection.cursor()
            for query in (query_track, query_playlist, query_pl_tr):
                cursor.execute(query, (file_name,))
            self.__connection.commit()
        except Exception as e:
            raise ec.DataBaseError(f"Error while adding pl_tr data. {type(e).__name__}: {e}")

    def add_tr_art_from_csv(self, file_name):
        query_artist = '''
        LOAD DATA LOCAL INFILE %s
        IGNORE INTO TABLE artist
        CHARACTER SET utf8mb4
        FIELDS TERMINATED BY ';'
        IGNORE 1 LINES
        (@tr_id, @tr_name, art_id, art_name);'''
        query_art_tr = '''LOAD DATA LOCAL INFILE %s
        IGNORE INTO TABLE art_tr
        CHARACTER SET utf8mb4
        COLUMNS TERMINATED BY ';'
        IGNORE 1 LINES
        (tr_id, @tr_name, art_id, @art_name);'''
        try:
            self.__connection.reconnect()
            cursor = self.__connection.cursor()
            for query in (query_artist, query_art_tr):
                cursor.execute(query, (file_name,))
            self.__connection.commit()
        except Exception as e:
            raise ec.DataBaseError(f"Error while adding track data. {type(e).__name__}: {e}")

    def get_events(self, number_of_tracks=1, only_future=True):
        if only_future:
            if_only_future = 'AND ev_date >= NOW()'
        else:
            if_only_future = ''
        query = f'''WITH art_imp AS (
                SELECT art_id, count(tr_name) AS importance
                FROM artist_all_info
                GROUP BY art_id
            )
            SELECT DISTINCT * FROM
            event_all_info JOIN art_imp USING (art_id)
            WHERE importance >=%s
            {if_only_future}
            ORDER BY importance DESC;'''
        try:
            return self.__dataframe_from_query(query, params=(number_of_tracks,))
        except Exception as e:
            raise ec.DataBaseError(f"Error while trying to fetch event data. {type(e).__name__}: {e}")

    def get_artists(self, number_of_tracks=4):
        query = '''SELECT art_name, count(tr_name) AS number_of_tracks
                FROM artist_all_info GROUP BY art_id 
                HAVING number_of_tracks >=%s
                ORDER BY number_of_tracks DESC;'''
        try:
            return self.__dataframe_from_query(query, params=(number_of_tracks,))
        except Exception as e:
            raise ec.DataBaseError(f"Error while trying to fetch event data. {type(e).__name__}: {e}")

    def close_connection(self):
        try:
            self.__connection.close()
        except Exception as e:
            raise ec.DataBaseError(f"Error while closing connection. {type(e).__name__}: {e}")
