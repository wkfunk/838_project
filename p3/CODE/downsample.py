import py_entitymatching as em

songs = em.read_csv_metadata('songs.csv',low_memory = False)
tracks = em.read_csv_metadata('tracks.csv',low_memory = False)

em.set_key(songs, 'id')
em.set_key(tracks, 'id')

sample_songs, sample_tracks = em.down_sample(songs, tracks, size=3500, y_param=1, show_progress=True)

em.to_csv_metadata(sample_songs,'C:/Users/Daniel/Documents/UW/838/Project/Stage3/data/song_sample.csv')
em.to_csv_metadata(sample_tracks,'C:/Users/Daniel/Documents/UW/838/Project/Stage3/data/track_sample.csv')