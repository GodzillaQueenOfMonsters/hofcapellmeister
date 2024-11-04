# hofcapellmeister
connects infos from your music streaming habits (Deezer) to concerts of your favourite artists in your area (for Vienna, www.volume.at)

## how to use
### info
#### database structure:
![relational model in the third normal form for the database joining data from both sources](./hcm_relational_model.jpg)

### Set up database
Set up a MariaDB server with your preferred method and create a database.\
Per default, the database is running locally, database name is *hofcapellmeister*, user is *hcm* with password *db_connector*.\
Default values can be changed in the ***hcm.cnf*** file.

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
  ```
- to quit (**after** *hofcapellmeister* is finished - it needs a running MariaDB server to work!), type:
  ```mysql
  EXIT;
  ```
If user root has a password, and you don't want to put this password into the cnf file, you can create a user just for access to this database; for example:
- enter MariaDB from command shell:
  ```console
  mysql -u root -p
  ```
- in the MariaDB terminal, type:
  ```mysql
  CREATE DATABASE hofcapellmeister;
  create user 'hcm'@'localhost' identified by 'db_connector';
  grant all on hofcapellmeister.* to hcm@localhost;
  ```
- *CAUTION*: remember to adjust the ***hcm.cnf*** file accordingly!

### Set up/run program
- set up docker environment from the main folder of your *hofcapellmeister* repository (after ensuring that Docker is running):
  ```console
  docker build -t hcm .
  ```

- run docker container in interactive mode and mount directory:\
*NOTE*: You might run into issues if you have any spaces in the path of your working directory. This is a known issue with Docker. Furthermore, the syntax for mounting your working directory might vary slightly, depending on the operating system and/or console you are working from.
  - for Windows:
    ```console
    docker run -it --rm -v .:/hcm hcm bash
    ```
  - on Linux:
    ```console
    docker run -it --rm --network="host" -v /${PWD}:/hcm hcm bash
    ```
- run ***main.py***: The playlist IDs from Deezer must be provided via a textfile in the same folder as ***api_logger.py***, containing one ID per line.
For trying out the functionality, you can use ***sample_playlist_id.txt***.
*NOTE*: The data for the plots are filtered by number of tracks (how many tracks from this artist are found in the database, assuming that the more tracks of this artist are in your playlist, the more important this artist is to you) to provide a reasonable output with readable plots.
Currently, the filter is set to at least 1 tracks for future events and 1 tracks for the overview of your favorite artists directly in the ***main.py*** script, which works fine for the sample playlist used for development. You will probably have to change these parameters to get reasonable output.
  ```console
  python main.py <textfile_with_playlist_ids>
  ```
### Overview of modules
- ***module api_logger.py***: extract data from playlists via *Deezer API* and save it to csv files in ppl_tr_data and tr_art_data, in subdirectories named by playlist id;\

- ***module web_logger.py***: get previous and future event data via *volume.at webscraping* for a list of artists (directly from database) and save it to csv files in events_data;\

- ***module save_data.py***: create all tables for database if they don't exist;\
save all data from folders ***events_data***, ***pl_tr_data***, ***tr_art_data*** to the *hofcapellmeister* database;\

- ***module plot_data.py***: get data for future events and for artists and plot an overview in ***result_plots.png***\

- ***module db_connector.py***: contains a class with all methods for connecting to the database;\

## ideas for further improvement
- add webscraping from arena.wien homepage and/or others to complete missing details
- if no events can be found for users favourite artists, get events for recommended/similar artists
- get all playlists and favourite songs from a user (with user login)
- try to implement the project also for other music streaming services 
