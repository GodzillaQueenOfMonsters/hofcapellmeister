from db_connector import ConnectorMariaDB
import error_classes as ec
import matplotlib.pyplot as plt

number_of_tracks = 6

try:
    hcm_db = ConnectorMariaDB()
    df_events = hcm_db.get_ev_imp()
    # print(df_events.head(20))
    df_artists = hcm_db.get_art_imp(number_of_tracks=number_of_tracks)
    # print(df_artists.head(20))
except ec.DataBaseError as e:
    print(type(e).__name__, e)
finally:
    hcm_db.close_connection()

try:
    plt.figure(figsize=(15, 4))
    plt.subplot(1, 2, 1)
    plt.hist(df_events['ev_date'], bins=40, color='hotpink')
    plt.xlabel('event date')
    plt.ylabel('number')
    plt.title(
        label="future events",
        fontdict={"fontsize": 14},
        pad=15
    )

    plt.subplot(1, 2, 2)
    pie_values = df_artists['number_of_tracks']
    plt.pie(
        pie_values,
        labels=df_artists['art_name'].str.replace('$', '\\$'),
        # colors=['gold', 'silver', 'peru'],
        autopct=lambda x: '{:.0f} tracks'.format(x*pie_values.sum()/100),
        textprops={'fontsize': 9},
        pctdistance = 0.8,
        radius = 1.2
    )
    plt.title(
        label=f"favorite artists ({number_of_tracks} or more tracks)",
        fontdict={"fontsize": 14},
        pad=15
    )

    plt.savefig('result_plots.png')
except NameError:
    pass
