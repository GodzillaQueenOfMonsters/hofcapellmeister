from db_connector import ConnectorMariaDB
import error_classes as ec
import matplotlib.pyplot as plt

db_path = 'hofcapellmeister'
user = 'root'
password = ''
host = 'host.docker.internal'

try:
    hcm_db = ConnectorMariaDB(db_name=db_path, user=user, password=password, host=host)
    df_events = hcm_db.get_events()
    print(df_events.head(20))
    df_artists = hcm_db.get_artists(number_of_tracks=6)
    print(df_artists.head(20))
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
    plt.pie(
        df_artists['number_of_tracks'],
        labels=df_artists['art_name'].str.replace('$', '\\$'),
        # colors=['gold', 'silver', 'peru'],
        autopct='%1.2f%%',
        textprops={'fontsize': 12}
    )
    plt.title(
        label="favorite artists",
        fontdict={"fontsize": 14},
        pad=15
    )

    plt.savefig('result_plots.png')
except NameError:
    pass
