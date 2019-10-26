import math
import numpy as np

def tf_idt(word, name, word_person_count, person_word_count):
    """ Returns the tf-idt for a given word and a name"""
    wpc = word_person_count
    pwc = person_word_count
    if not name in wpc[word]:
        return 0.0
    n_names = len(pwc)
    n_words_person = len(pwc[name])
    n_person_word = len(wpc[word])
    name_word_count = wpc[word][name]
    word_name_count = pwc[name][word]
    return name_word_count / n_words_person * math.log(n_names / n_person_word, 10)


def tf_idt_words(name, word_person_count, person_word_count) -> np.array:
    """ Returns an array with tf_idt for every word for given name"""
    wpc = word_person_count
    pwc = person_word_count
    n_words = len(wpc)
    tf_idts = np.zeros(n_words)
    for word, i in zip(wpc.keys(), range(n_words)):
        if not word in pwc[name]:
            continue
        tf_idts[i] = tf_idt(word, name, wpc, pwc)
    return tf_idts

