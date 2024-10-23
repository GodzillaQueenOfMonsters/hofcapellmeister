import requests
import pandas as pd
import os
import sys
import time
from tqdm import tqdm


# import json


# send a GET-request to an url and return response as json file
def return_json(url):
    # checks whether request was successful (Statuscode 200).
    try:
        response = requests.get(url)  # , params=param)
        if response.status_code == 200:
            json_file = response.json()
            return json_file
        else:
            raise ConnectionError('A problem with the url occurred.')
    except ConnectionError as e:
        raise ConnectionError(e)


# extract track info from playlist json file
def extract_tr_info(jsonfile):
    if jsonfile:
        pl_tracks = jsonfile['tracks']['data']
        tr_list = []
        for track in pl_tracks:
            tr_id = track['id']
            tr_dict = {
                'pl_id': jsonfile['id'],
                'pl_name': jsonfile['title'],
                'tr_id': tr_id,
                'tr_name': track['title']
            }
            tr_list.append(tr_dict)
        return pd.DataFrame(tr_list)
    else:
        raise TypeError()


# extract artist info from track json file
def extract_art_info(jsonfile):
    if jsonfile:
        art_list = []
        try:
            tr_artists = jsonfile['contributors']
            for artist in tr_artists:
                # print(artist['name'])
                art_dict = {
                    'tr_id': jsonfile['id'],
                    'tr_name': jsonfile['title'],
                    'art_id': artist['id'],
                    'art_name': artist['name']
                }
                art_list.append(art_dict)
        except KeyError as e:
            print(f"KeyError: {e}. Trying field 'artist'.")
            try:
                art_dict = {
                    'tr_id': jsonfile['id'],
                    'tr_name': jsonfile['title'],
                    'art_id': jsonfile['artist']['id'],
                    'art_name': jsonfile['artist']['name']
                }
                art_list.append(art_dict)
            except KeyError as e:
                raise KeyError(e)
        return pd.DataFrame(art_list)
    else:
        raise TypeError()


# create result folder if not exists and save list of dicts as csv
def save_df_as_csv(info_df, table_name, name_addition=''):
    if not os.path.exists(f'{table_name}_data'):
        print(f"created directory '{table_name}_data'")
        os.mkdir(f'{table_name}_data')
    info_df.to_csv(f'{table_name}_data/{table_name}_{name_addition}.csv', mode='w', sep=';', index=False)


with open(sys.argv[1], 'r') as input_file:
    pl_ids = input_file.readlines()

artist_df_list = []
for pl_id in pl_ids:
    pl_id = pl_id.strip()
    # create url for deezer api for a specific playlist
    pl_url = f'https://api.deezer.com/playlist/{pl_id}'
    # read playlist info
    try:
        pl_info = return_json(pl_url)
        # with open(f'{pl_id}.json', mode='w') as pl_json:
        #     pl_json.write(json.dumps(pl_info, indent=4))
        pl_tr_df = extract_tr_info(pl_info)
    except TypeError:
        print(f"Json file for {pl_id} returned empty.")
    except KeyError as e:
        print(f"Playlist {pl_id} could not be read: {e} does not exist.")

    if not pl_tr_df.empty:
        # check for length of playlist in order to avoid exceeding api request limit
        if pl_tr_df.shape[0] > 50:
            playlist_is_long = True
        else:
            playlist_is_long = False
        # save track ids and track names with playlist id and playlist name
        pl_name = pl_tr_df['pl_name'][0]
        save_df_as_csv(pl_tr_df, table_name='pl_tr', name_addition=f'{pl_id}_{pl_name}')

        # create url for deezer api for each track on playlist
        tr_art_list = []
        for _, tr_id in tqdm(pl_tr_df['tr_id'].items()):
            try:
                tr_url = f'https://api.deezer.com/track/{tr_id}'
                # read track info
                tr_info = return_json(tr_url)
                tr_art_df = extract_art_info(tr_info)
                if not tr_art_df.empty:
                    tr_art_list.append(tr_art_df)
                if playlist_is_long:
                    time.sleep(0.05)
            except TypeError as e:
                print(f"Json file for {tr_id} returned empty.")
            except KeyError as e:
                print(f"Track {tr_id} could not be read: {e} does not exist.")

        # save track ids and track names with playlist id and playlist name
        tr_art_df_per_pl = pd.concat(tr_art_list, ignore_index=True)
        # print(set(tr_art_df_per_pl['art_name']))
        save_df_as_csv(tr_art_df_per_pl, table_name='tr_art', name_addition=f'{pl_id}_{pl_name}')

        artist_df_list.append(tr_art_df_per_pl[['art_id', 'art_name']].drop_duplicates(ignore_index=True))
        # with open('artists.txt', 'a') as write_artists:
        #     for artist in tr_art_df_per_pl['art_id', 'art_name'].drop_duplicates(inplace=True, ignore_index=True):
        #         write_artists.write(artist + '\n')
            # write_artists.writelines(set(tr_art_df_per_pl['art_name']))
artist_df = pd.concat(artist_df_list, ignore_index=True).drop_duplicates(ignore_index=True)
artist_df.to_csv(f'artists.csv', mode='w', sep=';', index=False)
# print(artist_df)