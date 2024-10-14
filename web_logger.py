import requests
from bs4 import BeautifulSoup

artist = 'within%20temptation'
url = f'https://www.volume.at/?s={artist}'
# url = 'https://www.volume.at/?s=within%20temptation'

response = requests.get(url)
print('response is here')
# Parsing the HTML
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)