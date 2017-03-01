import sys
import csv
import ml

pos_prefix = "<+>"
pos_suffix = "</>"
neg_prefix = "<->"
neg_suffix = "</>"

def main(argv):
    assert len(argv) == 3, "Usage: python extract_features.py <train_file> <test_file>"
    
    (train_fname, test_fname) = argv[1:]

    # list of lists, e.g.
    # [['Arun', 'himself', 'is', 'a', 'pretty', 'funny', 'and', ... ] ,
    #  ['Bach', 'is', 'still', 'in', 'charge', 'of', 'the', 'homework', ... ] ,
    #  ...
    # ]
    train = process_file(argv[1])
    (train_names, train_samples, train_labels) = extract_features(train)

    test = process_file(argv[2])
    (test_names, test_samples, test_labels) = extract_features(test)
    
    # write output to file, including header
    #write_file(train_names, train_samples, train_labels, train_fname + ".feat")
    #write_file(test_names, test_samples, test_labels, test_fname + ".feat")

    # do n-fold cross validation
    n_fold_cv(2, train_samples, train_labels)

    # process with scikit
    run_test(train_samples, train_labels, test_samples, test_labels)

def run_test(train_samples, train_labels, test_samples, test_labels):
    algs = ml.run(train_samples, train_labels, test_samples, test_labels)

    print ""

    fmt = "{0:30}{1:<20}{2:<20}"
    print "Test set results:\n----------------------------------------"
    print fmt.format("Algo", "P", "R")
    for alg in algs:
        key = alg.__class__.__name__
        print fmt.format(key, alg.P(), alg.R())

def n_fold_cv(n, samples, labels):
    (sample_groups, sample_labels) = split_groups(n, samples, labels)
    
    p = {}
    r = {}
    sz = {}

    for i in range(n):
        train_samples = [x for j in range(n) if j != i for x in sample_groups[j]]
        train_labels = [x for j in range(n) if j != i for x in sample_labels[j]]

        test_samples = sample_groups[i]
        test_labels = sample_labels[i]

        algs = ml.run(train_samples, train_labels, test_samples, test_labels)

        for alg in algs:
            key = alg.__class__.__name__
            if key not in p:
                p[key] = 0.0
                r[key] = 0.0

            p[key] += alg.P()
            r[key] += alg.R()

    fmt = "{0:30}{1:<20}{2:<20}"
    print "N-fold Cross Validation:\n----------------------------------------"
    print fmt.format("Algo", "P", "R")
    for key in p.keys():
        print fmt.format(key, p[key]/n, r[key]/n)


def split_groups(n, samples, labels):
    import random

    random.seed(100)
    r = range(len(samples))
    random.shuffle(r)

    groups = [r[i::n] for i in xrange(n)]

    sample_groups = [[samples[i] for i in l] for l in groups]
    sample_labels = [[labels[i] for i in l] for l in groups]

    return (sample_groups, sample_labels)

def write_file(names, samples, labels, fname):
    with open(fname, 'wb') as f:
        csv_writer = csv.writer(f)

        # header line
        csv_writer.writerow(names + ["label"])

        assert len(samples) == len(labels), "Length mismatch."

        for (sample, label) in zip(samples, labels):
            csv_writer.writerow(sample + [label])

def extract_features(L):
    fns = get_fns()

    (samples, labels) = apply_features(L, fns)

    names = [fn.__name__ for fn in fns]
    return (names, samples, labels)

def apply_features(L, fns):
    L_strip = strip_lines(L)
    
    samples = []
    labels = []

    for lineno,line in enumerate(L):
        for i,word in enumerate(line):
            pos = is_pos(word)
            neg = is_neg(word)

            if pos or neg:
                samples.append([apply_feature(fn, L_strip[lineno], i) for fn in fns])

                # add label
                if pos:
                    labels.append(1)
                else:
                    labels.append(0)
    return (samples, labels)
                
def apply_feature(fn, line, i):
    return cast(fn(line, i))

def cast(val):
    if isinstance(val, (bool)):
        return int(val)
    else:
        return val

def strip_lines(L):
    newL = [line[:] for line in L[:]]
    for line in newL:
        for i,word in enumerate(line):
            if is_pos(word) or is_neg(word):
                line[i] = strip_word(word)
    return newL

def strip_word(w):
    if is_pos(w):
        return w[len(pos_prefix) : len(w) - len(pos_suffix)]
    elif is_neg(w):
        return w[len(neg_prefix) : len(w) - len(neg_suffix)]
    else:
        assert False

def is_pos(w):
    return w.startswith(pos_prefix) and w.endswith(pos_suffix)

def is_neg(w):
    return w.startswith(neg_prefix) and w.endswith(neg_suffix)

def get_fns():
    import features
    return [item for item in \
            [getattr(features, i) for i in dir(features)] \
            if callable(item)]

def process_file(fname):
    with open(fname, 'r') as f:
        lines = f.read().splitlines()
    lines = map(dequote, lines)
    words = map(lambda x : x.split(" "), lines)

    return words

def dequote(line):
    if line.startswith('"') and line.endswith('"'):
        return line[1:-1]
    else:
        return line

if __name__ == "__main__":
    main(sys.argv)
