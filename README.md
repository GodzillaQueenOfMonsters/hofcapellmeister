# hofcapellmeister
connects infos from your music streaming habits (planned: tidal) to concerts of your favourite artists in your area (planned: Vienna, oeticket)

First steps:
- set up docker environment:
docker build -t hcm .
- run docker container in interactive mode and mount directory for development:
winpty docker run -it --rm -v /c/Users/am-user347/Documents/hofcapellmeister:/hcm hcm bash

Next steps:
- set up basic functionality via tidal API (alternative: Deezer): module api_logger.py, including a README file
- set up basic functionality via webscraping of oeticket (alternative: bandsintown): module web_logger.py
- conceptualize a relational model in the third normal form for a database joining data from both sources
- write DDL statements for all required tables for MariaDB (alternative: PostgreSQL)
- join data into database: module safe_data.py
- write unittest for safe_data.py
- visualize part of the data
