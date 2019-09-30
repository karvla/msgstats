import regex as re
import pickle
import math
from itertools import combinations
from functools import reduce
from datetime import timedelta, datetime, date
import indexing
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from setup import path_cache, path_home
import os


def tf_idt(word, name):
    """ Returns the tf-idt for a given word and a name"""
    if not name in wpc[word]:
        return 0.0
    n_names = len(pwc)
    n_words_person = len(pwc[name])
    n_person_word = len(wpc[word])
    name_word_count = wpc[word][name]
    word_name_count = pwc[name][word]
    return name_word_count / n_words_person * math.log(n_names / n_person_word, 10)


def tf_idt_words(name) -> np.array:
    """ Returns an array with tf_idt for every word for given name"""
    n_words = len(wpc)
    tf_idts = np.zeros(n_words)
    for word, i in zip(wpc.keys(), range(n_words)):
        if not word in pwc[name]:
            continue
        tf_idts[i] = tf_idt(word, name)
    return tf_idts


def person_tf_idt() -> dict:
    """ Returns a dict with a tf_idt-array for every person"""
    pti = dict()
    for name in pwc.keys():
        pti[name] = tf_idt_words(name)
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
    """ Prints the words with the highest tf-idt for a given name """
    words = pwc[name].keys()
    tf = list(map(lambda w: tf_idt(w, name), words))
    for i in sorted(zip(words, tf), key=lambda x: x[1], reverse=True)[:N]:
        print(i)


def print_names_with_most_words_written(N=20):
    name_word_sum = [(name, sum(pwc[name].values())) for name in pwc.keys()]
    print("Most words written:")
    for i in sorted(name_word_sum, key=lambda x: x[1], reverse=True)[:N]:
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
    plt.draw()


def plot_freq(names, date_dict, ylabel="", yscale="linear"):
    for name in names:
        x, y = moving_avg(date_dict[name]["to"])
        p = plt.plot(x, y, label=("to " + name))
        p[-1].get_color()

        x, y = moving_avg(date_dict[name]["from"])
        plt.plot(x, y, label="from " + name)

    plt.ylabel(ylabel)
    plt.yscale(yscale)
    plt.legend()
    plt.draw()


def moving_avg(date_dict, N=30):
    """ Takes a dict containing dates as keys and
        returns a list or dates and the moving average
        for each date with period N """
    w = N // 2 - 1
    start_date = min(date_dict.keys())
    end_date = max(date_dict.keys())
    n_days = (end_date - start_date).days
    dates_full = [start_date + timedelta(days=n) for n in range(n_days)]
    y = [0 if d not in date_dict else date_dict[d] for d in dates_full]

    y_avg = [sum(y[n - w : n + 1 + w]) / N for n in range(w, n_days - w)]
    d_avg = dates_full[w:-w]
    return d_avg, y_avg


def print_conv(
    name, 
    start_date=date(1970, 1, 1),
    end_date=date.today(),
    filter_func=lambda x: True
):
    """ Prints the conversation beween dates,
        filters the messages according to filter_func. """
    start = start_date
    end = end_date
    msg_tot = pts[name]["to"] + pts[name]["from"]
    msg_sorted = sorted(msg_tot, key=lambda x: x["timestamp"])

    for msg in msg_sorted:
        msg_date = datetime.fromtimestamp(msg["timestamp"])
        name = msg["name"]
        content = msg["content"]
        n_words = msg["n_words"]
        if start < msg_date.date() and msg_date.date() < end and filter_func(msg):
            print(name + " " + msg_date.strftime("%Y-%m-%d, %H:%M:%S") + ":")
            print(content)
            print()


if __name__ == "__main__":
    os.chdir("/")
    with open(path_cache, 'rb') as f:
        pwc, wpc, pti, pts, mpd, wpd = pickle.load(f)
