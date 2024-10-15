import requests
import pandas as pd
import os


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
        return pl_title, track_list
    else:
        return


# create result folder if not exists and save list of dicts as csv
def save_list_of_dicts_as_csv(list_of_dicts, name_addition=''):
    if list_of_dicts:
        if not os.path.exists('playlist_data'):
            print("created directory 'playlist_data'")
            os.mkdir('playlist_data')
        try:
            pd.DataFrame(list_of_dicts).to_csv(f'playlist_data/playlist_{name_addition}.csv', mode='x', sep=';', index=False)
        except FileExistsError as e:
            print('File already exists!')
    else:
        return


# create url for deezer api for a specific playlist
# playlist_id = 12738706081
playlist_id = 10400967982
url = f'https://api.deezer.com/playlist/{playlist_id}'

playlist_name, track_list = extract_track_info(return_json(url))
# print(playlist_name)
# for track in track_list:
#     print(track)

save_list_of_dicts_as_csv(track_list, name_addition=playlist_name)
