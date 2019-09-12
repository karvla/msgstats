import os
import json
from stop_words import get_stop_words

inbox_path = 'messages/inbox/'
stopwords = set((get_stop_words('en'))).union(set(get_stop_words('sv'))) # TODO: Make not hardcoded

def _words(text): return list(re.finditer(r'\p{L}+', text.lower()))

def _decode(string): return string.encode('latin_1').decode('utf-8')

def _add_word_count(index, word):
    "Adds 1 to count and returns the index" 
    if word in stopwords: return index
    if word in index:
        index[word] += 1
    else:
        index[word] = 1
    return index

def word_count(name):
    """ word --> count"""
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
    """ person -->  word --> nr"""
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

def word_people_count(pwc):
    """ word --> person --> count"""
    wpc = dict()
    for name in pwc.keys():
        for word in pwc[name]:
            if word in wpc:
                wpc[word][name] = pwc[name][word] 
            else:
                wpc[word] = dict([(name, pwc[name][word])])
    return wpc
