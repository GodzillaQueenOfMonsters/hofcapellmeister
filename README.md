# hofcapellmeister
connects infos from your music streaming habits (Deezer) to concerts of your favourite artists in your area (for Vienna, www.volume.at)

## how to use
### info
#### hcm_relational_model.jpg
relational model in the third normal form for the database joining data from both sources;
#### hcm_create_database.txt
DDL statements to create *hofcapellmeister* database in *MariaDB* (for information only, not executed)
### Set up database
Set up a MariaDB server with your preferred method and create a database with the name *hofcapellmeister*.
Here is one example, using xampp:
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
- set up docker environment from the main folder of your *hofcapellmeister* repository:
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

## ideas for further improvement
- add webscraping from arena.wien homepage and/or others to complete missing details
- prevent some of the faulty search results
- if no events can be found for users favourite artists, get events for recommended/similar artists
- get all playlists and favourite songs from a user (with user login)
- somehow get url to buy tickets to events (even though oeticket is ungrateful and doesn't like us)