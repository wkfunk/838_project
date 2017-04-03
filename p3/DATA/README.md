A and B are songs.csv and tracks.csv, taken from the provided Silicon Valley dataset. We downsampled them (`song_sample.csv`, 3038 tuples and `track_sample.csv`, 3500 tuples) using Magellan, but the schemas remained identical.

All tuple pairs that survive the blocking step: `candidate_pairs.csv` (543 tuples)
All tuple pairs in the sample you have taken, together with the labels, one label per each tuple pair: `golden_labeled_all_missing_removed.csv` (533 tuples)
Two files that describe the sets I and J: `I.txt` and `J.txt`