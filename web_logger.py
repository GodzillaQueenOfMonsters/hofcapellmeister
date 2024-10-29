import pandas as pd
import requests
import os
from db_connector import ConnectorMariaDB
import error_classes as ec
from bs4 import BeautifulSoup
import re


# send a GET-request to an url and return response as soup file
def return_soup(url):
    try:
        response = requests.get(url)
        # checks whether request was successful (Statuscode 200).
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
        else:
            raise ConnectionError('A problem with the url occurred.')
    except ConnectionError as err:
        print(f"ConnectionError: {err}")


def get_event_data(soup):
    soup = soup.find_all('section', class_="collection section--grid")
    result_dict = {}
    for section in soup:
        category = section.find('h2', class_='section-header__title').text
        res_key = category.lower().replace('events für ', '').replace(' ', '_').replace('"', '')
        dates = []
        names = []
        locations = []
        for name_location in section.find_all('h3', class_='item__title'):
            try:
                location = name_location.find('small', class_='item__location').text.strip()
            except AttributeError:
                location = None
            locations.append(location)
            try:
                event_name = name_location.find('span').text.strip()
            except AttributeError:
                event_name = None
            names.append(event_name)
        for event_date in section.find_all('div', class_='item__date'):
            dates.append(event_date.text.strip())

        # print()
        df = pd.DataFrame({'event_name': names,
                           'date': dates,
                           'location': locations})
        result_dict[res_key] = df
    return result_dict


def save_df_as_csv(events_df, name_addition=''):
    if not os.path.exists('events_data'):
        print("created directory 'events_data'")
        os.mkdir('events_data')
    events_df.to_csv(f'events_data/events_{name_addition}.csv', mode='w', sep=';', index=False)


def prep_str_for_url(raw_str):
    nasty_chars = r'[^\w\s]'
    return re.sub(nasty_chars, '', raw_str).replace(' ', '+')


artists = None
try:
    hcm_db = ConnectorMariaDB()
    artists = hcm_db.get_artist()
except ec.DataBaseError as e:
    print(type(e).__name__, e)
finally:
    hcm_db.close_connection()

for _, artist in artists.iterrows():
    art_id = artist['art_id']
    search_term = prep_str_for_url(artist['art_name'])

    # create url to search for artist events at volume.at
    a_url = f'https://www.volume.at/?s={search_term}&post_type=event'
    # read events info
    try:
        results = get_event_data(return_soup(a_url))
        # save results
        for key, dataframe in results.items():
            if not dataframe.empty:
                dataframe['search_term'] = search_term
                dataframe['art_id'] = art_id
                save_df_as_csv(dataframe, name_addition=key)
            else:
                print(f"No events found for: {key}")
    except TypeError:
        pass
