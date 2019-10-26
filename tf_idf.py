from setup import path_cache, path_home
import math
import numpy as np
import argparse
import os
import pickle
import matplotlib.pyplot as plt

"""
Imports person_word_count, word_person_count, and person_tf_idt
"""
with open(path_cache, "rb") as f:
    pwc, wpc, pti, _, _, _ = pickle.load(f)


def tf_idf(word, name):
    """ Returns the tf-idf for a given word and a name"""
    if not name in wpc[word]:
        return 0.0
    n_names = len(pwc)
    n_words_person = len(pwc[name])
    n_person_word = len(wpc[word])
    name_word_count = wpc[word][name]
    word_name_count = pwc[name][word]
    return name_word_count / n_words_person * math.log(n_names / n_person_word, 10)


def tf_idf_words(name) -> np.array:
    """ Returns an array with tf_idf for every word for given name"""
    n_words = len(wpc)
    tf_idfs = np.zeros(n_words)
    for word, i in zip(wpc.keys(), range(n_words)):
        if not word in pwc[name]:
            continue
        tf_idfs[i] = tf_idf(word, name)
    return tf_idfs


def person_tf_idf() -> dict:
    """ Returns a dict with a tf_idf-array for every person"""
    pti = dict()
    for name in pwc.keys():
        pti[name] = tf_idf_words(name)
    return pti


def sparse_cossine(v1, v2) -> float:
    """ Returns cosine for a pair of sparse vectors """
    abs_v1 = np.sqrt(sum(map(lambda x: x * x, v1)))
    abs_v2 = np.sqrt(sum(map(lambda x: x * x, v2)))
    dot_prod = 0.0
    for a, b in zip(v1, v2):
        if not (a and b):
            continue
        dot_prod += a * b
    return float(dot_prod / (abs_v1 * abs_v2))


def print_tf_score(name, N=20):
    """ Prints the words with the highest tf-idf for a given name """
    words = pwc[name].keys()
    tf = list(map(lambda w: tf_idf(w, name), words))
    for i in sorted(zip(words, tf), key=lambda x: x[1], reverse=True)[:N]:
        print(i)


def plot_cosim_vs_words(self_name):
    """ Plots the number of written words vs. the 
        cosinus similarity between all names and self_name """
    fig, ax = plt.subplots()
    ax = fig.add_subplot(111)
    for name in pwc.keys():
        if name == self_name:
            continue
        x = sparse_cossine(pti[self_name], pti[name])
        y = sum(pwc[name].values())
        label = ax.annotate(name, xy=(x, y), fontsize=12, ha="center")
        plt.scatter(x, y)
    plt.xlabel("tf-idf cossine similarity against " + self_name)
    plt.ylabel("#words written")
    plt.yscale("log")
    plt.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Uses tf-idf on the chat history, where every person is a document."
    )
    parser.add_argument(
        "-t",
        dest="f",
        action="store_const",
        const=print_tf_score,
        default=print,
        help="displays the words with highest tf-idf score for a given name.",
    )

    parser.add_argument(
        "-p",
        dest="f",
        action="store_const",
        const=plot_cosim_vs_words,
        default=print,
        help="plots total number of words written vs. td-idf cosine similariy",
    )

    parser.add_argument(
            "name",
            type=str,
            nargs='+',
            help = "the name of a person"
    )

    args = parser.parse_args()
    args.f(" ".join(args.name))

