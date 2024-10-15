# hofcapellmeister
connects infos from your music streaming habits (Deezer) to concerts of your favourite artists in your area (for Vienna, www.volume.at)

## project documentation - work in progress
### Previous steps
- set up docker environment:
docker build -t hcm .
- run docker container in interactive mode and mount directory for development:
winpty docker run -it --rm -v /${PWD}:/hcm hcm bash
- **module api_logger.py**: extract data from playlists and save it to csv file in playlist_data
  usage:
  ```console
  python api_logger playlist_ids.txt
  ```
- **module web_logger.py**: set up webscraping connection to volume.at

### current work in progress
- set up basic functionality via webscraping of volume.at: module web_logger.py

### TODO api_logger.py
- implement extraction of multiple artists from one track (currently: only first artist is extracted)
- implement handling of special characters etc. in band names
- write docu how to use it

### TODO next week
- conceptualize a relational model in the third normal form for a database joining data from both sources
- write DDL statements for all required tables for MariaDB (alternative: PostgreSQL)
- join data into database: module safe_data.py
- visualize part of the data

### TODO last week
- write unit tests
- clean up code and project structure
- clean up documentation
- more beautiful visualization
- implement more features
- last step: publish repository