import helper

def is_first_word(L, i):
    return i == 0

def is_last_word(L, i):
    return i == len(L) - 1

def length(L, i):
    return len(L[i])

def preceded_by_is_are(L, i):
    return helper.preceded_by(['is', 'was', 'are', 'were'])(L, i)

def preceded_by_modifier(L, i):
    return helper.preceded_by(['too', 'pretty', 'very', 'really'])(L, i)

def preceded_by_a_an(L, i):
    return helper.preceded_by(['a', 'an', 'the'])(L, i)

def preceded_by_this_that(L, i):
    return helper.preceded_by(['this', 'that'])(L, i)

def is_common_word(L, i):
    return helper.is_in_list(['of', 'a', 'an', 'and', 'to', 'the'])(L, i)

def is_followed_by_common_linking_verb(L, i):
    return helper.followed_by(['am','is','was','are','will','were','become','becomes','became','seem','seems','seemed'])(L, i)

def is_preceded_by_common_linking_verb(L, i):
    return helper.preceded_by(['am','is','was','are','will','were','become','becomes','became','seem','seems','seemed'])(L, i)

def ends_in_ly(L, i):
    return helper.ends_with("ly")(L, i)

def ends_in_able(L, i):
    return helper.ends_with("able")(L, i)

def ends_in_ible(L, i):
    return helper.ends_with("ible")(L, i)

def ends_in_al(L, i):
    return helper.ends_with("al")(L, i)

def ends_in_an(L, i):
    return helper.ends_with("an")(L, i)

def ends_in_ar(L, i):
    return helper.ends_with("ar")(L, i)

def ends_in_ent(L, i):
    return helper.ends_with("ent")(L, i)

def ends_in_ful(L, i):
    return helper.ends_with("ful")(L, i)

def ends_in_ic(L, i):
    return helper.ends_with("ic")(L, i)

def ends_in_ical(L, i):
    return helper.ends_with("ical")(L, i)

def ends_in_ine(L, i):
    return helper.ends_with("ine")(L, i)

def ends_in_ile(L, i):
    return helper.ends_with("ile")(L, i)

def ends_in_ive(L, i):
    return helper.ends_with("ive")(L, i)

def ends_in_less(L, i):
    return helper.ends_with("less")(L, i)

def ends_in_ous(L, i):
    return helper.ends_with("ous")(L, i)

def ends_in_some(L, i):
    return helper.ends_with("some")(L, i)

def ends_in_ing(L, i):
    return helper.ends_with("ing")(L, i)

def ends_in_ed(L, i):
    return helper.ends_with("ed")(L, i)

def is_adjective(L, i):
    adjectives = helper.make_set("word_lists/adjectives.txt")
    return L[i].lower() in adjectives

def is_pronouns(L, i):
    pronouns_mods = helper.make_set("word_lists/pronouns_mod.txt")
    return L[i].lower() in pronouns_mods

def is_verb(L, i):
    verbs_mod = helper.make_set("word_lists/verbs_mod.txt")
    return L[i].lower() in verbs_mod

def is_preposition(L, i):
    prepositions_mod = helper.make_set("word_lists/prepositions_mod.txt")
    return L[i].lower() in prepositions_mod

def is_noun(L, i):
    nouns_mod = helper.make_set("word_lists/nouns_mod.txt")
    return L[i].lower() in nouns_mod

def is_adverb(L, i):
    adverbs_mod = helper.make_set("word_lists/adverbs_mod.txt")
    return L[i].lower() in adverbs_mod


