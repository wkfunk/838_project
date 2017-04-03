import py_entitymatching as em

songs = em.read_csv_metadata('data/song_sample.csv',low_memory = False)
tracks = em.read_csv_metadata('data/track_sample.csv',low_memory = False)	

"""
kwargs = {'encoding':'utf-8'}
golden = em.read_csv_metadata('data/track_sample.csv',low_memory = False,
					**kwargs)	
print golden.head()
"""



em.set_key(songs, 'id')
em.set_key(tracks, 'id')

ob = em.OverlapBlocker()
candidate_pairs = ob.block_tables(songs, tracks, 'name', 'name', 
					word_level=True, 
					overlap_size=1, 
                    l_output_attrs=['name', 'artist', 'year'], 
                    r_output_attrs=['name', 'artist','year'],
					allow_missing=True,
                    show_progress=True)
				
print len(candidate_pairs)
				
candidate_pairs = ob.block_candset(candidate_pairs, 'artist', 'artist',
					word_level=True, 
					overlap_size=1, 
					show_progress=True)

					
print len(candidate_pairs)

#em.to_csv_metadata(reduced_pairs,'C:/Users/Daniel/Documents/UW/838/Project/Stage3/data/pairs_after_ob_title_and_artist.csv')



block_f = em.get_features_for_blocking(songs,tracks)	
block_c = em.get_attr_corres(songs,tracks)
block_t = em.get_tokenizers_for_blocking()
block_s = em.get_sim_funs_for_blocking()

atypes1 = em.get_attr_types(songs)
atypes2 = em.get_attr_types(tracks)

block_f = em.get_features(songs, tracks, atypes1, atypes2, block_c, block_t, block_s)

rb = em.RuleBasedBlocker()
rb.add_rule(["name_name_jac_dlm_dc0_dlm_dc0(ltuple, rtuple) < 0.3"], block_f)

candidate_pairs = rb.block_candset(candidate_pairs,
                    show_progress=True)
					
print len(candidate_pairs)
				
#em.to_csv_metadata(candidate_pairs,'C:/Users/Daniel/Documents/UW/838/Project/Stage3/data/candidate_pairs.csv')

print candidate_pairs.head()

dbg = em.debug_blocker(candidate_pairs,songs,tracks,output_size = 50)
print dbg.head(20)

