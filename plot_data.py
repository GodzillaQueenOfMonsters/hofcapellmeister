from db_connector import ConnectorMariaDB
import error_classes as ec
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

num_of_tracks_events = 1
num_of_tracks_artists = 1
try:
    hcm_db = ConnectorMariaDB()
    df_events = hcm_db.get_ev_imp(number_of_tracks=num_of_tracks_events)
    # print(df_events.head(20))
    df_artists = hcm_db.get_art_imp(number_of_tracks=num_of_tracks_artists)
    # print(df_artists.head(20))
except ec.DataBaseError as e:
    print(type(e).__name__, e)
finally:
    hcm_db.close_connection()

try:
    # plt.figure(figsize=(10, 7))
    fig, axs = plt.subplots(2, 1, figsize=(10, 7))

    for artist in set(df_events['art_name']):
        filt_ev = df_events[df_events['art_name'] == artist]
        p = axs[0].bar(filt_ev['ev_date'], filt_ev['importance'], label=artist)
        axs[0].bar_label(p, labels=filt_ev['art_name'], rotation=90, rotation_mode='anchor', label_type='edge', padding=-30, fontsize=8)
        # print(artist)
    # axs[0].label_params()
    axs[0].tick_params(axis='x', labelsize=8)
    axs[0].set_xlabel('event date')
    axs[0].set_xticks(df_events['ev_date'])
    axs[0].set_xticklabels(df_events['ev_date'], rotation=90, ha='right', va='center', rotation_mode='anchor')
    # for _, event in df_events['ev_date'].items():
    #     ax.set_xticks([event])
    axs[0].yaxis.set_major_locator(MaxNLocator(integer=True))
    axs[0].set_ylabel('number of tracks')
    # ax.legend(loc='upper center')
    axs[0].set_title(
        label="future events",
        fontdict={"fontsize": 14},
        pad=15
    )

    # plt.subplot(2, 1, 2)
    pie_values = df_artists['number_of_tracks']
    axs[1].pie(
        pie_values,
        labels=df_artists['art_name'].str.replace('$', '\\$'),
        # colors=['gold', 'silver', 'peru'],
        autopct=lambda x: '{:.0f} tracks'.format(x*pie_values.sum()/100),
        textprops={'fontsize': 9},
        pctdistance = 0.8,
        radius = 1.2
    )
    axs[1].set_title(
        label=f"favorite artists ({num_of_tracks_artists} or more tracks)",
        fontdict={"fontsize": 14},
        pad=15
    )
    # plt.tight_layout()
    fig.tight_layout()
    fig.savefig('result_plots.png')
except NameError:
    pass
