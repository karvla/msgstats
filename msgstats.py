import os
import json
import regex as re
import pickle
import math
from itertools import combinations
from functools import reduce
import polyglot
from stop_words import get_stop_words

inbox_path = 'messages/inbox/'
me = 'Arvid Larsson'
stopwords = set((get_stop_words('en'))).union(set(get_stop_words('sv')))

def _words(text): return list(re.finditer(r'\p{L}+', text.lower()))

def _decode(string): return string.encode('latin_1').decode('utf-8')

def _add_word_count(index, word):
    if word in stopwords: return index
    if word in index:
        index[word] += 1
    else:
        index[word] = 1
    return index

def word_count(name):
    index = dict()
    for dir_name, subdirs, thread in os.walk(inbox_path):
        for fname in thread:
            path = '/'.join([dir_name, fname])
            if not re.findall('.json', path): continue
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
                if 'messages' not in data: continue
                for msg in data['messages']:
                    sender_name = _decode(msg['sender_name'])
                    if sender_name == name and msg['type'] == 'Generic' and 'content' in msg:
                        content = _decode(msg['content'])
                        [_add_word_count(index, word.group()) for word in _words(content.lower())]
    return index
            

def people_word_count():
    index = dict()
    for dir_name, subdirs, thread in os.walk(inbox_path):
        for fname in thread:
            path = '/'.join([dir_name, fname])
            if not re.findall('.json', path): continue
            with open(path, encoding='utf-8') as f:
                data = json.load(f)
                if 'messages' not in data: continue
                for msg in data['messages']:
                    if 'sender_name' in msg:
                        name = _decode(msg['sender_name'])
                        if name in index:
                            continue 
                        else:
                            index[name] = word_count(name)
    return index 

def word_people_count():
    wpc = dict()
    for name in pwc.keys():
        for word in pwc[name]:
            if word in wpc:
                wpc[word][name] = pwc[name][word] 
            else:
                wpc[word] = dict([(name, pwc[name][word])])
    return wpc

def td_idt(word, name):
    if not name in wpc[word]: return 0.0
    n_names = len(pwc)
    n_words_person = len(pwc[name])
    n_person_word = len(wpc[word])
    name_word_count = wpc[word][name]
    word_name_count = pwc[name][word]
    return name_word_count/n_words_person * math.log(n_names/n_person_word, 10)

def print_td_score(name, N=20):
    words = pwc[name].keys()
    td = list(map(lambda w: td_idt(w, name), words))
    for i in sorted(zip(words, td), key=lambda x: x[1], reverse=True)[:N]:
        print(i)

def most_words_written(N=20):
    name_word_sum = [(name, sum(pwc[name].values())) for name in pwc.keys()]
    print("Most words written:")
    for i in sorted(name_word_sum, key=lambda x : x[1], reverse=True)[:N]:
        print(i)

if __name__ == "__main__":
    filename = 'people_word_count'

    try:
        f = open(filename, 'rb')
        pwc = pickle.load(f)
        f.close()
    except:
        print("Index file not found. Indexing, may take a while..", end = '')
        pwc = people_word_count()
        with open(filename, 'wb') as f:
            pickle.dump(pwc, f)
        print("Done!")
        


    wpc = word_people_count()
    

