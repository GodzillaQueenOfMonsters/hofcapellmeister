import pandas as pd
import requests
import os
from hcm.db_connector import ConnectorMariaDB
import hcm.error_classes as ec
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
    except Exception as err:
        print(f"Error occurred when connecting to the url {url}: {type(err).__name__} {err}")


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
        df = pd.DataFrame({'event_name': names, 'date': dates, 'location': locations})
        result_dict[res_key] = df
    return result_dict


def save_df_to_csv(events_df, name_addition=''):
    if not os.path.exists('events_data'):
        print("created directory 'events_data'")
        os.mkdir('events_data')
    events_df.to_csv(f'events_data/events_{name_addition}.csv', mode='w', sep=';', index=False)


def prep_str_for_url(raw_str):
    nasty_chars = r'[^\w\s]'
    return re.sub(nasty_chars, '', raw_str).replace(' ', '+')


def is_valid_return(return_string, query_term):
    query_term = query_term.replace('+', ' ')
    regex_search_term_standalone = r'(\b' + re.escape(query_term) + r'\b)'
    is_invalid = re.search(regex_search_term_standalone, return_string, re.IGNORECASE)
    if is_invalid:
        return False
    else:
        return True


def get_artist_info():
    try:
        hcm_db = ConnectorMariaDB()
        artists = hcm_db.get_artist()
        hcm_db.close_connection()
        return artists
    except ec.DataBaseError as e:
        print(type(e).__name__, e)
        return None


# read events info
def read_and_save_event_info(art_id, search_term, url):
    try:
        results = get_event_data(return_soup(url))

        # filter results/sanity check, then save data to csv
        for key, dataframe in results.items():
            if not dataframe.empty:
                # create a column checking whether the event_name contains the search term as a standalone word
                isvalid_column = dataframe.apply(lambda x: is_valid_return(x['event_name'], search_term), axis=1)

                # drop all rows which likely not contain a result that is actually referring to a concert of the band
                valid_dataframe = dataframe.drop(dataframe[isvalid_column].index)

                if not valid_dataframe.empty:
                    # add columns with the search term the query was using and the corresponding artist_id
                    valid_dataframe['search_term'] = search_term
                    valid_dataframe['art_id'] = art_id

                    # save data to csv
                    save_df_to_csv(valid_dataframe, name_addition=key)

                else:
                    print(f"No valid events found for: {key}")
            else:
                print(f"No events found for: {key}")
    except TypeError:
        pass


try:
    artists = get_artist_info()
    for _, artist in artists.iterrows():
        art_id = artist['art_id']
        search_term = prep_str_for_url(artist['art_name'])
        # create url to search for artist events at arena.wien
        a_url = f'https://arena.wien/Home/Event-List?search-term={search_term}'
        read_and_save_event_info(art_id, search_term, a_url)
except AttributeError:
    pass
