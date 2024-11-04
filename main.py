from hcm.api_logger import create_overwrite_dir, return_json, playlist_recursion
from hcm.save_data import save_playlist_data, save_event_data
from hcm.web_logger import get_artist_info, prep_str_for_url, read_and_save_event_info
from hcm.plot_data import get_dfs_for_plotting, plot_event_and_artist_overview
import sys

# set variables for saving data to the database
date_format = '%d. %b %Y'
event_dir = r'/hcm/events_data/'
pl_tr_dir = r'/hcm/pl_tr_data/'
tr_art_dir = r'/hcm/tr_art_data/'

# set variables for plotting data
num_of_tracks_events = 1
num_of_tracks_artists = 1

# read playlist ids from textfile provided with program call
with open(sys.argv[1], 'r') as input_file:
    p_ids = input_file.readlines()

# loop over all playlist ids
for pid in p_ids:
    pid = pid.strip()

    # create folder for playlist
    create_overwrite_dir('pl_tr', pid)
    create_overwrite_dir('tr_art', pid)

    # create url for deezer api for a specific playlist
    n_url = f'https://api.deezer.com/playlist/{pid}'
    purl = f'https://api.deezer.com/playlist/{pid}/tracks'

    # read playlist info
    pname = return_json(n_url)['title']
    playlist_recursion(purl, pid, pname)

save_playlist_data(pl_tr_dir, tr_art_dir)

# run web_logger for each playlist id
try:
    artists = get_artist_info()
    for _, artist in artists.iterrows():
        art_id = artist['art_id']
        search_term = prep_str_for_url(artist['art_name'])
        # create url to search for artist events at volume.at
        a_url = f'https://www.volume.at/?s={search_term}&post_type=event'
        read_and_save_event_info(art_id, search_term, a_url)
except AttributeError:
    pass

save_event_data(date_format, event_dir)

try:
    df_events, df_artists = get_dfs_for_plotting(num_of_tracks_events, num_of_tracks_artists)
    plot_event_and_artist_overview(df_events, df_artists, num_of_tracks_events, num_of_tracks_artists)
except NameError:
    pass
