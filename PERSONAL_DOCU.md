## TODO
### general
- maybe orchestrate everything from a ***main.py*** file
- finish up README
- last step: publish repository

### web_logger.py
- check/improve handling of special characters
- review try except blocks: exception handling was partly copy-pasted from ***api_logger.py***, parts can be removed or modified
- (write unittests)

### api_logger.py
- better exception handling in case of requests.exceptions.ConnectionError: Max retries exceeded with url
- find out why only 400 lines were written in ***artists.csv***
- review try except blocks
- (write unittests)

### db_connector.py
- read connection variables from configfile

### save_data.py
- **write unittests**

### plot_data.py
- pie chart: show number of tracks instead of percent
- useful plot for events