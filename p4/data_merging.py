import pandas

def merge(fname1, # name of first file
          fname2, # name of second file
          cnames1, # column names in table 1
          cnames2, # column names in table 2
          merging_fn): #functions to merge columns

    f1 = pandas.read_csv(fname1)
    f2 = pandas.read_csv(fname2)

    f1_cols = list(f1.columns.values)
    f2_cols = list(f2.columns.values)

    # check that the input complies with our expectations:
    # 1) the lists of column names must match in length
    assert len(cnames1) == len(cnames2) and len(cnames2) == len(merging_fn), \
        "ERROR: Length of corresponding column lists must match: %d != %d." % \
        (len(cnames1), len(cnames2))
    # 2) the list of merging functions must be the same length
    assert all([col in f1_cols for col in cnames1]), \
        "ERROR: All columns given must be in list of actual column names: %s != %s" % \
        (str(cnames1), str(f1_cols))
    # 3) the input tables must be the same length (1:1 correspondence)
    assert len(f1) == len(f2), \
        "ERROR: Two data frames must have the same number of (corresponding) rows"

    # this is the resulting table that we will populate
    result = pandas.DataFrame()
    
    # loop over the columns in both tables which do NOT need to be merged, and populate them
    # in the resulting table
    for col in f1_cols:
        if col not in cnames1:
            result[col] = f1[col]
    for col in f2_cols:
        if col not in cnames2:
            result[col] = f2[col]

    # now, loop over all the columns that must be merged and do so
    for i in range(len(cnames1)):
        col1 = cnames1[i]
        col2 = cnames2[i]
        f = merging_fn[i]

        # construct the tuple pairs to be merged
        e = pandas.concat([f1[col1], f2[col2]], axis=1)        

        # perform the merging
        new_col = "%s_%s_merged" % (col1, col2)

        # insert into the table
        result[new_col] = e.apply(f, axis=1)
 
    return result

# These are the merging functions:
# 1) merge year with year:
#    simply return the tracks year, as songs has many missing values, while tracks 
#    has very few if any
def merge_years(x):
    songs_year = x[0]
    tracks_year = x[1]

    return tracks_year
 
# 2) merge artist with artists
#    simply return tracks_artist, since, if the pairs are a match, the song artist 
#    ought to match one of the artists in the tracks artist, which is actually a 
#    list of artists delimited by +   
def merge_artists(x):
    songs_artist = x[0]
    tracks_artist = x[1]

    return tracks_artist

# 3) merge title with name     
#    return the shorter of the two song names, a longer song name probably has something 
#    like a version of that song specified
def merge_names(x):
    songs_name = x[0]
    tracks_name = x[1]

    if len(songs_name) < len(tracks_name):
        return songs_name
    return tracks_name


# Perform the merging
result = merge('datasets/songs_for_merging.csv', 'datasets/tracks_for_merging.csv', 
      ['title', 'artist_name', 'year'],
      ['song', 'artists', 'year'],
      [merge_names, merge_artists, merge_years]
)

# Write the file to disk
result.to_csv("E.csv")

    
