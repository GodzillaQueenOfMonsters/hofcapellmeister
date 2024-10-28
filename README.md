# hofcapellmeister
connects infos from your music streaming habits (Deezer) to concerts of your favourite artists in your area (for Vienna, www.volume.at)

## project documentation
### Set up database
- relational model in the third normal form for the database joining data from both sources:\
***hcm_relational_model.jpg***
- DDL statements to create *hofcapellmeister* database in *MariaDB* (for information only):\
***hcm_create_database.txt***
- create database:
  - start xampp
  - start Apache, then MySQL
  - start shell from the xampp control panel
    ```console
    mysql -u root
    ```
  - create database:
    ```mysql
    CREATE DATABASE hofcapellmeister;
    USE hofcapellmeister;
    ```
### Set up/run program
- set up docker environment:
  ```console
  docker build -t hcm .
  ```
- run docker container in interactive mode and mount directory for development:
  ```console
  winpty docker run -it --rm -v /${PWD}:/hcm hcm bash
  ```
- ***module api_logger.py***: extract data from playlists via *Deezer API* and save it to csv files in ppl_tr_data and tr_art_data, respectively
  ```console
  python api_logger.py aram_pl.txt
  ```
- ***module web_logger.py***: get previous and future event data via *volume.at webscraping* for a list of artists (output from ***module api_logger.py***) and save it to csv files in events_data
  ```console
  python web_logger.py
  ```
- ***module save_data.py***: create all tables for database if they don't exist and save all data from folders ***events_data***, ***pl_tr_data***, ***tr_art_data*** to the *hofcapellmeister* database
  ```console
  python save_data.py
  ```
- ***module plot_data.py***: get data for future events and for artists and save plots in ***result_plots.png***
  ```console
  python plot_data.py
  ```

## TODO
### general
- maybe orchestrate everything from a ***main.py*** file
- last step: publish repository

### web_logger.py
- check/improve handling of special characters
- review try except blocks: exception handling was partly copy-pasted from ***api_logger.py***, parts can be removed or modified
- (write unittests)

### api_logger.py
- better exception handling in case of requests.exceptions.ConnectionError: Max retries exceeded with url
- find out why only 400 lines were written in ***artists.csv***
- review try except blocks
- write docu how to use it
- (write unittests)

### db_connector.py
- check if *create_hcm_tables* is finished before importing data
- read ddl for creating tables from textfile
- read connection variables from configfile

### save_data.py
- **write unittests**

### plot_data.py
- less artists for pie chart, show number of tracks instead of percent, useful plot for events

## ideas for further improvement
- add webscraping from arena.wien homepage and/or others to complete missing details
- prevent some of the faulty search results
- if no events can be found for users favourite artists, get events for recommended/similar artists
- get all playlists and favourite songs from a user (with user login)
- somehow get url to buy tickets to events (even though oeticket is ungrateful and doesn't like us)