import requests
from bs4 import BeautifulSoup

# artist = 'within%20temptation'
# url = f'https://www.volume.at/?s={artist}'
url = 'https://www.oeticket.com/events/konzerte-109/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

response = requests.get(url, headers=header)
print('response is here')
# Parsing the HTML
soup = BeautifulSoup(response.content, 'html.parser')
print(soup)
