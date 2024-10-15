import requests
import pandas as pd
import os
import sys


# send a GET-request to an url and return response as json file
def return_json(url):
    # param = {'q': playlist_number}
    # checks whether request was successful (Statuscode 200).
    try:
        response = requests.get(url)  # , params=param)
        if response.status_code == 200:
            json_file = response.json()
            return json_file
        else:
            raise ConnectionError('A problem with the url occurred.')
    except ConnectionError as e:
        print(f"ConnectionError: {e}")


# extract list of artists from jsonfile
def extract_track_info(jsonfile):
    if jsonfile:
        pl_title = jsonfile['title']
        pl_tracks = jsonfile['tracks']['data']
        track_list = []
        for track in pl_tracks:
            track_dict = {'title': track['title'],
                          'artist': track['artist']['name']}
            track_list.append(track_dict)
        return pl_title, pd.DataFrame(track_list)
    else:
        return


# create result folder if not exists and save list of dicts as csv
def save_df_as_csv(track_df, name_addition=''):
    if not track_df.empty:
        if not os.path.exists('playlist_data'):
            print("created directory 'playlist_data'")
            os.mkdir('playlist_data')
        try:
            track_df.to_csv(f'playlist_data/playlist_{name_addition}.csv', mode='x', sep=';', index=False)
        except FileExistsError:
            print('File already exists!')
    else:
        return


# playlist_id = 12738706081
# playlist_id = 10400967982
with open(sys.argv[1], 'r') as input_file:
    pl_ids = input_file.readlines()

for pl_id in pl_ids:
    pl_id = pl_id.strip()
    # create url for deezer api for a specific playlist
    url = f'https://api.deezer.com/playlist/{pl_id}'
    # read playlist info
    try:
        playlist_name, track_info = extract_track_info(return_json(url))
        # save results
        try:
            save_df_as_csv(track_info, name_addition=f'{playlist_name}_id_{pl_id}')
        except FileExistsError:
            print('File already exists!')
    except KeyError as e:
        print(f"Playlist {pl_id} could not be read: {e} does not exist.")
    except TypeError:
        pass
    #
    # except NameError as e:
    #     print(f"{pl_id} is probably not a valid playlist id.")
