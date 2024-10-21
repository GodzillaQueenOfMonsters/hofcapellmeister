import pandas as pd
import requests
import os
import sys
from bs4 import BeautifulSoup


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
    if not events_df.empty:
        if not os.path.exists('events_data'):
            print("created directory 'events_data'")
            os.mkdir('events_data')
        try:
            events_df.to_csv(f'events_data/events_{name_addition}.csv', mode='x', sep=';', index=False)
        except FileExistsError:
            print('File already exists!')
    else:
        return


# artist = 'within%20temptation'
# artist = 'halloween'
# artist = 'laraduna'
# a_url = f'https://www.volume.at/?s={artist}&post_type=event'
#
# results = get_dumplings(return_soup(a_url))
# for key, value in results.items():
#     save_df_as_csv(value, name_addition=key)


# with open(sys.argv[1], 'r') as input_file:
#     artists = input_file.readlines()
#
# for artist in artists:
#     artist = artist.strip().replace(' ', '+')
#     # create url to search for artist events at volume.at
#     a_url = f'https://www.volume.at/?s={artist}&post_type=event'
#     # read events info
#     try:
#         results = get_event_data(return_soup(a_url))
#         # save results
#         for key, dataframe in results.items():
#             try:
#                 save_df_as_csv(dataframe, name_addition=key)
#             except FileExistsError:
#                 print('File already exists!')
#     except KeyError as e:
#         print(f"Playlist {artist} could not be read: {e}")
#     except TypeError:
#         pass
