# hofcapellmeister
connects infos from your music streaming habits (Deezer) to concerts of your favourite artists in your area (for Vienna, www.volume.at)

## project documentation - work in progress
### Previous steps
- set up docker environment:
  ```console
  docker build -t hcm .
  ```
- run docker container in interactive mode and mount directory for development:
  ```console
  winpty docker run -it --rm -v /${PWD}:/hcm hcm bash
  ```
- **module api_logger.py**: extract data from playlists via **Deezer API** and save it to csv file in playlist_data
  ```console
  python api_logger playlist_ids.txt
  ```
- **module web_logger.py**: get previous and future event data via **volume.at webscraping** for a given list of artists and save it to csv files in events_data
  ```console
  python web_logger artists.txt
  ```

### TODO web_logger.py
- implement handling of special characters etc. in band names (here or in **api_logger.py**)
- use output of **api_logger.py** directly as input
- review try except blocks: exception handling was partly copy-pasted from **api_logger.py**, parts can be removed or modified
- unittests would be great

### TODO api_logger.py
- implement extraction of multiple artists from one track (currently: only first artist is extracted)
- implement handling of special characters etc. in band names
- write docu how to use it
- unittests would be great

### TODO next week
- conceptualize a relational model in the third normal form for a database joining data from both sources
- write DDL statements for all required tables for MariaDB (alternative: PostgreSQL)
- join data into database: module **safe_data.py**
- visualize part of the data

### TODO last week
- write unit tests
- clean up code and project structure
- clean up documentation
- more beautiful visualization
- implement more features:
  - if no events can be found for users favourite artists, get events for recommended/similar artists
  - get all playlists and favourite songs from a user (with user login)
  - somehow get url to buy tickets to events (even though oeticket is ungrateful and doesn't like us)
  - order/prioritize events according to how much the user likes them (how many songs from this artist are in the playlists)
- last step: publish repository