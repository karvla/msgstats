import regex as re
import pickle
import math
from itertools import combinations
from functools import reduce
import indexing
import numpy as np
import matplotlib.pyplot as plt

me = 'Arvid Larsson'


def tf_idt(word, name):
    if not name in wpc[word]: return 0.0
    n_names = len(pwc)
    n_words_person = len(pwc[name])
    n_person_word = len(wpc[word])
    name_word_count = wpc[word][name]
    word_name_count = pwc[name][word]
    return name_word_count/n_words_person * math.log(n_names/n_person_word, 10)

def tf_idt_words(name) -> np.array:
    n_words = len(wpc)
    tf_idts = np.zeros(n_words)
    for word, i in zip(wpc.keys(), range(n_words)):
        if not word in pwc[name]: continue
        tf_idts[i] = tf_idt(word, name)
    return tf_idts

def person_tf_idt() -> dict:
    pti = dict()
    for name in pwc.keys():
        pti[name] = tf_idt_words(name)
    return pti

def sparse_cossine(v1, v2) -> float:
    """ Returns cosine for a pair of sparse vectors """
    abs_v1 = np.sqrt(sum(map(lambda x: x*x, v1)))
    abs_v2 = np.sqrt(sum(map(lambda x: x*x, v2)))
    dot_prod = 0.0
    for a, b, in zip(v1, v2):
        if not (a and b): continue
        dot_prod += a*b
    return float(dot_prod/(abs_v1*abs_v2))

def print_tf_score(name, N=20):
    words = pwc[name].keys()
    tf = list(map(lambda w: tf_idt(w, name), words))
    for i in sorted(zip(words, tf), key=lambda x: x[1], reverse=True)[:N]:
        print(i)

def most_words_written(N=20):
    name_word_sum = [(name, sum(pwc[name].values())) for name in pwc.keys()]
    print("Most words written:")
    for i in sorted(name_word_sum, key=lambda x : x[1], reverse=True)[:N]:
        print(i)

def plot_cosim_vs_words(self_name):
    fig, ax = plt.subplots()
    ax = fig.add_subplot(111)
    for name in pwc.keys():
        if name == self_name: continue
        x = sparse_cossine(pti[self_name], pti[name])
        y = sum(pwc[name].values())
        label = ax.annotate(name, xy=(x, y), fontsize=12, ha="center")
        plt.scatter(x, y)
    plt.xlabel("tf-idf cossine similarity against " + self_name)
    plt.ylabel("#words written")
    plt.yscale("log")
    plt.show()

if __name__ == "__main__":
    filename = 'index_file'

    try:
        f = open(filename, 'rb')
        pwc, wpc, pti = pickle.load(f)
        f.close()
    except:
        print("Index file not found. Indexing, may take a while..", end = '')
        pwc = indexing.people_word_count()
        wpc = indexing.word_people_count(pwc)
        pti = person_tf_idt()
        index = (pwc, wpc, pti)
        with open(filename, 'wb') as f:
            pickle.dump(index, f)
        print("Done!")
    spacer = "{0:<10} {1:<10}"



    

        


