# hofcapellmeister
connects infos from your music streaming habits (Deezer) to concerts of your favourite artists in your area (for Vienna, www.volume.at)

## how to use
### info
#### hcm_relational_model.jpg
relational model in the third normal form for the database joining data from both sources;

### Set up database
Set up a MariaDB server with your preferred method and create a database.\
Per default, the database is running locally, database name is *hofcapellmeister*, user is *root* with no password.\
Default values can be changed in the ***config.txt*** file.

Here is one example how you can set up the database, using xampp:
- run xampp
- from the xampp control panel, start Apache, then MySQL
- start a shell from the xampp control panel, then type:
  ```console
  mysql -u root
  ```
- to create the database, type:
  ```mysql
  CREATE DATABASE hofcapellmeister;
  USE hofcapellmeister;
  ```
- to quit (**after** *hofcapellmeister* is finished - it needs a running MariaDB server to work!), type:
  ```mysql
  EXIT;
  ```
For Linux:
- enter MariaDB from command shell:
  ```console
  mysql -u root -p -S /var/run/mysqld/mysqld.sock
  ```
- to create the database, type:
  ```mysql
  CREATE DATABASE hofcapellmeister;
  create user 'hcm'@'localhost' identified by 'db_connector';
  grant all on hofcapellmeister.* to hcm@localhost;
  ```
### Set up/run program
- set up docker environment from the main folder of your *hofcapellmeister* repository:
  ```console
  docker build -t hcm .
  ```
- run docker container in interactive mode and mount directory for development (on Windows, via git-bash):
  ```console
  winpty docker run -it --rm -v /${PWD}:/hcm hcm bash
  ```
- run docker container in interactive mode and mount directory for development (on Linux):
  ```console
  docker run -it --rm --network="host" -v $(pwd):/hcm hcm bash

  ```
- ***module api_logger.py***: extract data from playlists via *Deezer API* and save it to csv files in ppl_tr_data and tr_art_data, in subdirectories named by playlist id
  ```console
  python api_logger.py aram_pl.txt
  ```
- ***module web_logger.py***: get previous and future event data via *volume.at webscraping* for a list of artists (directly from database) and save it to csv files in events_data
  ```console
  python web_logger.py
  ```
- ***module save_data.py***: create all tables for database if they don't exist;\
save all data from folders ***events_data***, ***pl_tr_data***, ***tr_art_data*** to the *hofcapellmeister* database
  ```console
  python save_data.py
  ```
- ***module plot_data.py***: get data for future events and for artists and save plots in ***result_plots.png***
  ```console
  python plot_data.py
  ```

## ideas for further improvement
- add webscraping from arena.wien homepage and/or others to complete missing details
- prevent some of the faulty search results
- if no events can be found for users favourite artists, get events for recommended/similar artists
- get all playlists and favourite songs from a user (with user login)
- somehow get url to buy tickets to events (even though oeticket is ungrateful and doesn't like us)
