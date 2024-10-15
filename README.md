# hofcapellmeister
connects infos from your music streaming habits (Deezer) to concerts of your favourite artists in your area (for Vienna, www.volume.at)

## project documentation - work in progress
### Previous steps
- set up docker environment:
docker build -t hcm .
- run docker container in interactive mode and mount directory for development:
winpty docker run -it --rm -v /${PWD}:/hcm hcm bash
- set up connection via Deezer API: module api_logger.py, 
- set up connection via webscraping of volume.at: module web_logger.py

### current work in progress
- try to get webscraping from www.oeticket.com:
**IDEA**: https://www.zenrows.com/blog/python-requests-user-agent#set-user-agent
error log: see textfile error_log_oeticket_web_logger.py.txt

### TODO this week
- set up basic functionality via Deezer API: module api_logger.py, including documentation
- set up basic functionality via webscraping of volume.at: module web_logger.py

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