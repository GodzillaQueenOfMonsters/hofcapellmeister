import mysql.connector
import pandas as pd
# from adodbapi.examples.db_table_names import databasename

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
                allow_local_infile = True
            )
            # cursor = self.__connection.cursor()
        except Exception as e:
            raise ec.DataBaseError(f"Error while connecting to server. {type(e).__name__}: {e}")
        self.__create_hcm_tables()
        # finally:
        #     self.close_connection()


    def __create_hcm_tables(self):
        try:
            cursor = self.__connection.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlist (
                pl_id INT PRIMARY KEY,
                pl_name VARCHAR(100) NOT NULL
                );

            CREATE TABLE IF NOT EXISTS track (
                tr_id INT PRIMARY KEY,
                tr_name VARCHAR(100) NOT NULL
                );

            CREATE TABLE IF NOT EXISTS artist (
                art_id INT PRIMARY KEY,
                art_name VARCHAR(100) NOT NULL
                );

            CREATE TABLE IF NOT EXISTS event (
                ev_id INT AUTO_INCREMENT PRIMARY KEY,
                ev_name VARCHAR(100) NOT NULL,
                ev_date DATE NOT NULL,
                ev_location VARCHAR(100) NOT NULL,
                UNIQUE(ev_name, ev_date, ev_location)
                );

            CREATE TABLE IF NOT EXISTS art_ev (
                art_id INT,
                ev_id INT,
                PRIMARY KEY(art_id, ev_id),
                FOREIGN KEY(art_id) REFERENCES artist(art_id),
                FOREIGN KEY(ev_id) REFERENCES event(ev_id)
                );

            CREATE TABLE IF NOT EXISTS art_tr (
                art_id INT,
                tr_id INT,
                PRIMARY KEY(art_id, tr_id),
                FOREIGN KEY(art_id) REFERENCES artist(art_id),
                FOREIGN KEY(tr_id) REFERENCES track(tr_id)
                );

            CREATE TABLE IF NOT EXISTS pl_tr (
                pl_id INT,
                tr_id INT,
                PRIMARY KEY(pl_id, tr_id),
                FOREIGN KEY(pl_id) REFERENCES playlist(pl_id),
                FOREIGN KEY(tr_id) REFERENCES track(tr_id)
                );
            ''')
            # self.__connection.commit()
        except Exception as e:
            raise ec.DataBaseError(f"Error while creating tables. {type(e).__name__}: {e}")

    # adds event data directly via insert statements; requires list of tuples or pandas DataFrame object
    def add_events(self, events, date_format):
        # date_format = '%d. %b %Y'
        if isinstance(events, pd.DataFrame):
            events = events.to_records(index=False).tolist()
        try:
            self.__connection.reconnect()
            cursor = self.__connection.cursor()
            query = f'''INSERT INTO event (ev_name, ev_date, ev_location) VALUES (%s, STR_TO_DATE(%s, '{date_format}'), %s)'''
            cursor.executemany(query, events)
            self.__connection.commit()
        except Exception as e:
            raise ec.DataBaseError(f"Error while adding events. {type(e).__name__}: {e}")

    def add_events_from_csv(self, file_name, date_format='%d. %b %Y'):
        try:
            self.__connection.reconnect()
            cursor = self.__connection.cursor()
            # cursor.execute("show global variables like 'opt_local_infile';")
            # return cursor.fetchall()
            query = f'''load data local infile '{file_name}'
            ignore into table event
            columns terminated by ';'
            ignore 1 lines
            (ev_name, @ev_date, ev_location)
            set ev_date=(SELECT STR_TO_DATE(@ev_date, '{date_format}')); '''
            cursor.execute(query)
            self.__connection.commit()
            # return cursor.fetchall()
        except Exception as e:
            raise ec.DataBaseError(f"Error while adding events. {type(e).__name__}: {e}")


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