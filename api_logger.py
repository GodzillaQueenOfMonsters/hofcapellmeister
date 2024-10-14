import requests
import pandas

# send a GET-request to deezer api
def return_artists_json(playlist_number):
    url = f'https://api.deezer.com/playlist/{playlist_number}'
    # param = {'q': playlist_number}
    # checks whether request was successful (Statuscode 200).
    try:
        response = requests.get(url)#, params=param)
        if response.status_code == 200:
            artist_json = response.json()
            return artist_json
        else:
            raise ConnectionError('A problem with the url occurred.')
    except ConnectionError as e:
        print(f"ConnectionError: {e}")

print(return_artists_json(12738706081))