def make_set(fname):
    s = set()
    with open(fname, 'r') as f:
        for line in f:
            s.add(line.strip().split("\t")[0])
    return s

def ends_with(suff):
    def f(L, i):
        return L[i].lower().endswith(suff)
    return f

def is_in_list(words):
    def f(L, i):
        return L[i].lower() in words
    return f

def preceded_by(words):
    def f(L, i):
        return i > 0 and L[i-1].lower() in words
    return f

def followed_by(words):
    def f(L, i):
        return i < len(L) - 1 and L[i+1].lower() in words
    return f


    
