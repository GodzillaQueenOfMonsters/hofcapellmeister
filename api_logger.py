import requests
import pandas as pd
import os
import sys
import shutil
import time
from tqdm import tqdm
import json


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
def extract_tr_info(jsonfile, pl_id, pl_name):
    try:
        new_url = jsonfile['next']
    except KeyError:
        new_url = None
    pl_tracks = jsonfile['data']
    tr_list = []
    for track in pl_tracks:
        tr_dict = {
            'pl_id': pl_id,
            'pl_name': pl_name,
            'tr_id': track['id'],
            'tr_name': track['title']
        }
        tr_list.append(tr_dict)
    name_add = ''
    if new_url:
        name_add += new_url[-3:].replace('=', '')
    return new_url, name_add, pd.DataFrame(tr_list)


# extract artist info from track json file
def extract_art_info(jsonfile):
    art_list = []
    try:
        tr_artists = jsonfile['contributors']
        for artist in tr_artists:
            art_dict = {
                'tr_id': jsonfile['id'],
                'tr_name': jsonfile['title'],
                'art_id': artist['id'],
                'art_name': artist['name']
            }
            art_list.append(art_dict)
    except KeyError as e:
        raise KeyError(e)
        # try:
        #     art_dict = {
        #         'tr_id': jsonfile['id'],
        #         'tr_name': jsonfile['title'],
        #         'art_id': jsonfile['artist']['id'],
        #         'art_name': jsonfile['artist']['name']
        #     }
        #     art_list.append(art_dict)
        # except KeyError as e:
        #     raise KeyError(e)
    return pd.DataFrame(art_list)


# create result folder if not exists and overwrite subdirectory
def create_overwrite_dir(table_name, file_id):
    base_dir = f'{table_name}_data'
    sub_dir = f'{base_dir}/{file_id}'
    if not os.path.exists(base_dir):
        os.mkdir(f'{table_name}_data')
        print(f"created directory '{table_name}_data'")
    if os.path.exists(sub_dir):
        shutil.rmtree(sub_dir)
        print(f"Overwriting '{sub_dir}'")
    os.mkdir(sub_dir)


# save list of dicts as csv
def save_df_as_csv(info_df, file_path, name_addition=''):
    file_path = f'{file_path}_{name_addition}.csv'
    info_df.to_csv(file_path, mode='w', sep=';', index=False)


def playlist_recursion(pl_url, pl_id, pl_name):
    # read playlist info
    new_url = None
    try:
        # pl_info = return_json(pl_url)
        # with open(f'{pl_id}.json', mode='w') as pl_json:
        #     pl_json.write(json.dumps(pl_info,
        #     indent=4))
        new_url, name_add, pl_tr_df = extract_tr_info(return_json(pl_url), pl_id, pl_name)
        # save track ids and track names with playlist id and playlist name
        save_df_as_csv(pl_tr_df, file_path=f'pl_tr_data/{pl_id}/{pl_id}_{pl_name}', name_addition=name_add)
        # create url for deezer api for each track on playlist
        tr_art_list = []
        time.sleep(0.5)
        for _, tr_id in tqdm(pl_tr_df['tr_id'].items()):
            try:
                tr_url = f'https://api.deezer.com/track/{tr_id}'
                # read track info
                tr_info = return_json(tr_url)
                tr_art_df = extract_art_info(tr_info)
                if not tr_art_df.empty:
                    tr_art_list.append(tr_art_df)
            except KeyError as e:
                print(f"Track {tr_id} could not be read: {e} does not exist.")

        # save track ids and track names with playlist id and playlist name
        tr_art_df_per_pl_chunk = pd.concat(tr_art_list, ignore_index=True)
        save_df_as_csv(tr_art_df_per_pl_chunk, file_path=f'tr_art_data/{pl_id}/{pl_id}_{pl_name}', name_addition=name_add)

        # artist_df_list.append(tr_art_df_per_pl[['art_id', 'art_name']].drop_duplicates(ignore_index=True))
    except KeyError as e:
        print(f"Playlist {pl_url} could not be read: {e} does not exist.")
    if new_url:
        return playlist_recursion(new_url, pl_id, pl_name)
    else:
        return


with open(sys.argv[1], 'r') as input_file:
    pl_ids = input_file.readlines()

# artist_df_list = []
for pl_id in pl_ids:
    pl_id = pl_id.strip()
    create_overwrite_dir('pl_tr', pl_id)
    create_overwrite_dir('tr_art', pl_id)
    # create url for deezer api for a specific playlist
    name_url = f'https://api.deezer.com/playlist/{pl_id}'
    pl_url = f'https://api.deezer.com/playlist/{pl_id}/tracks'
    # read playlist info
    pl_name = return_json(name_url)['title']
    playlist_recursion(pl_url, pl_id, pl_name)

# artist_df = pd.concat(artist_df_list, ignore_index=True).drop_duplicates(ignore_index=True)
# artist_df.to_csv(f'artists.csv', mode='w', sep=';', index=False)
# print(artist_df)
