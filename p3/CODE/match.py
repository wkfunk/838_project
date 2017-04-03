import py_entitymatching as em

songs = em.read_csv_metadata('data/song_sample.csv',low_memory = False)
tracks = em.read_csv_metadata('data/track_sample.csv',low_memory = False)

em.set_key(songs, 'id')
em.set_key(tracks, 'id')

labeled_candidates = em.read_csv_metadata('data/golden_labeled_all_missing_removed.csv', key = '_id',ltable = songs, rtable = tracks, fk_ltable='ltable_id', fk_rtable='rtable_id')

IJ = em.split_train_test(labeled_candidates, train_proportion=0.7, random_state=0)
I = IJ['train']
J = IJ['test']

dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name='NaiveBayes')

feature_table = em.get_features_for_matching(songs, tracks)

H = em.extract_feature_vecs(I, 
                            feature_table=feature_table, 
                            attrs_after='gold',
                            show_progress=False)
							
result = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, 
        exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'],
        k=5,
        target_attr='gold', metric='precision', random_state=0)
		
L = em.extract_feature_vecs(J, feature_table=feature_table,
                            attrs_after='gold', show_progress=False)

lg.fit(table=H, 
       exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
       target_attr='gold')

predictions = lg.predict(table=L, exclude_attrs=['_id', 'ltable_id', 'rtable_id', 'gold'], 
              append=True, target_attr='predicted', inplace=False)

eval_result = em.eval_matches(predictions, 'gold', 'predicted')
em.print_eval_summary(eval_result)