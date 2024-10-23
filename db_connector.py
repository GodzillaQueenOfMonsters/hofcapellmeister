import mysql.connector
# import pymysql
import pandas as pd
# from adodbapi.examples.db_table_names import databasename

import error_classes as ec


class ConnectorMariaDB:
    def __init__(self, db_name, staging_name, user, password, host):
        self.__db_name = db_name
        self.__staging = staging_name
        try:
            self.__connection = mysql.connector.connect(
                database=self.__db_name,
                host=host,
                user=user,
                password=password,
                allow_local_infile=True
            )
            # cursor = self.__connection.cursor()
        except Exception as e:
            raise ec.DataBaseError(f"Error while connecting to server. {type(e).__name__}: {e}")
        try:
            self.__create_hcm_tables()
        except ec.DataBaseError as e:
            print(e)
        # try:
        #     self.__create_staging_tables()
        # except ec.DataBaseError as e:
        #     print(e)
        # finally:
        #     self.close_connection()

    def __create_hcm_tables(self):
        try:
            cursor = self.__connection.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist (
                pl_id BIGINT PRIMARY KEY,
                pl_name VARCHAR(100) NOT NULL
                );
            CREATE TABLE IF NOT EXISTS track (
                tr_id BIGINT PRIMARY KEY,
                tr_name VARCHAR(100) NOT NULL
                );
            CREATE TABLE IF NOT EXISTS artist (
                art_id BIGINT PRIMARY KEY,
                art_name VARCHAR(100) NOT NULL
                );
            CREATE TABLE IF NOT EXISTS event (
                ev_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                ev_name VARCHAR(100) NOT NULL,
                ev_date DATE NOT NULL,
                ev_location VARCHAR(100) NOT NULL,
                UNIQUE(ev_name, ev_date, ev_location)
                );
            CREATE TABLE IF NOT EXISTS art_ev (
                art_id BIGINT,
                ev_id BIGINT,
                PRIMARY KEY(art_id, ev_id),
                FOREIGN KEY(art_id) REFERENCES artist(art_id),
                FOREIGN KEY(ev_id) REFERENCES event(ev_id)
                );
            CREATE TABLE IF NOT EXISTS art_tr (
                art_id BIGINT,
                tr_id BIGINT,
                PRIMARY KEY(art_id, tr_id),
                FOREIGN KEY(art_id) REFERENCES artist(art_id),
                FOREIGN KEY(tr_id) REFERENCES track(tr_id)
                );
            CREATE TABLE IF NOT EXISTS pl_tr (
                pl_id BIGINT,
                tr_id BIGINT,
                PRIMARY KEY(pl_id, tr_id),
                FOREIGN KEY(pl_id) REFERENCES playlist(pl_id),
                FOREIGN KEY(tr_id) REFERENCES track(tr_id)
                );
            ''')
            # self.__connection.commit()
        except Exception as e:
            raise ec.DataBaseError(f"Error while creating hcm tables. {type(e).__name__}: {e}")

    # # adds event data directly via insert statements; requires list of tuples or pandas DataFrame object
    # def add_events(self, events, date_format):
    #     if isinstance(events, pd.DataFrame):
    #         events = events.to_records(index=False).tolist()
    #     try:
    #         self.__connection.reconnect()
    #         cursor = self.__connection.cursor()
    #         query = f'''INSERT INTO event (ev_name, ev_date, ev_location) VALUES (%s, STR_TO_DATE(%s, '{date_format}'), %s)'''
    #         cursor.executemany(query, events)
    #         self.__connection.commit()
    #     except Exception as e:
    #         raise ec.DataBaseError(f"Error while adding events. {type(e).__name__}: {e}")

    def add_events_from_csv(self, file_name, date_format='%d. %b %Y'):
        try:
            self.__connection.reconnect()
            cursor = self.__connection.cursor()
            cursor.execute("SET NAMES utf8mb4;")
            query = f'''load data local infile '{file_name}'
            ignore into table event
            CHARACTER SET utf8mb4
            columns terminated by ';'
            ignore 1 lines
            (ev_name, @ev_date, ev_location)
            set ev_date=(SELECT STR_TO_DATE(@ev_date, '{date_format}')); '''
            cursor.execute(query)
            self.__connection.commit()
            # return cursor.fetchall()
        except Exception as e:
            raise ec.DataBaseError(f"Error while adding events. {type(e).__name__}: {e}")

    def add_pl_tr_from_csv(self, file_name):
        try:
            self.__connection.reconnect()
            cursor = self.__connection.cursor()
            # cursor.execute(f"USE {self.__staging}")
            cursor.execute("SET NAMES utf8mb4;")
            query_pl_tr = f'''LOAD DATA LOCAL INFILE '{file_name}'
            IGNORE INTO TABLE pl_tr
            CHARACTER SET utf8mb4
            COLUMNS TERMINATED BY ';'
            IGNORE 1 LINES
            (pl_id, @pl_name, tr_id, @tr_name);'''
            query_track = f'''LOAD DATA LOCAL INFILE '{file_name}'
            IGNORE INTO TABLE track
            CHARACTER SET utf8mb4
            COLUMNS TERMINATED BY ';'
            IGNORE 1 LINES
            (@pl_id, @pl_name, tr_id, tr_name);'''
            query_playlist = f'''LOAD DATA LOCAL INFILE '{file_name}'
            IGNORE INTO TABLE playlist
            CHARACTER SET utf8mb4
            COLUMNS TERMINATED BY ';'
            IGNORE 1 LINES
            (pl_id, pl_name, @tr_id, @tr_name);'''
            # print(query)
            for query in (query_track, query_playlist, query_pl_tr):
                cursor.execute(query)
            self.__connection.commit()
            # return cursor.fetchall()
        except Exception as e:
            raise ec.DataBaseError(f"Error while adding pl_tr data. {type(e).__name__}: {e}")

    def add_tr_art_from_csv(self, file_name):
        try:
            self.__connection.reconnect()
            cursor = self.__connection.cursor()
            # cursor.execute(f"USE {self.__staging}")
            cursor.execute("SET NAMES utf8mb4;")
            query_artist = f'''LOAD DATA LOCAL INFILE '{file_name}'
            IGNORE INTO TABLE artist
            CHARACTER SET utf8mb4
            FIELDS TERMINATED BY ';'
            IGNORE 1 LINES
            (@tr_id, @tr_name, art_id, art_name);'''
            query_art_tr = f'''LOAD DATA LOCAL INFILE '{file_name}'
            IGNORE INTO TABLE art_tr
            CHARACTER SET utf8mb4
            COLUMNS TERMINATED BY ';'
            IGNORE 1 LINES
            (tr_id, @tr_name, art_id, @art_name);'''

            for query in (query_artist, query_art_tr):
                cursor.execute(query)
                print(query)
            self.__connection.commit()
            # return cursor.fetchall()
        except Exception as e:
            raise ec.DataBaseError(f"Error while adding track data. {type(e).__name__}: {e}")

        # finally:
        #     self.close_connection()

    # def get_movies_by_director(self, director):
    #     try:
    #         cursor = self.__connection.cursor()
    #         cursor.execute('SELECT * FROM movies WHERE director = %s;', (director,))
    #     except Exception as e:
    #         raise ec.DatabaseError(
    #             f"Error while trying to fetch movies directed by {director}. {type(e).__name__}: {e}")
    #     columns = [desc_list[0] for desc_list in cursor.description]
    #     return pd.DataFrame(cursor.fetchall(), columns=columns)
    #     # finally:
    #     #     self.close_connection()
    #
    # def delete_movie(self, movie_id):
    #     try:
    #         cursor = self.__connection.cursor()
    #         cursor.execute('DELETE FROM movies WHERE id=%s', (movie_id,))
    #         self.__connection.commit()
    #     except Exception as e:
    #         raise ec.DatabaseError(f"Error while trying to delete movie with id = {movie_id}. {type(e).__name__}: {e}")
    # finally:
    #     self.close_connection()

    def close_connection(self):
        try:
            self.__connection.close()
        except Exception as e:
            raise ec.DataBaseError(f"Error while closing connection. {type(e).__name__}: {e}")
