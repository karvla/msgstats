import os
import json
from stop_words import get_stop_words
import regex as re

inbox_path = "messages/inbox/"
stopwords = set((get_stop_words("en"))).union(
    set(get_stop_words("sv"))
)  # TODO: Make not hardcoded


def _words(text):
    return list(re.findall(r"\p{L}+", text.lower()))


def _decode(string):
    return string.encode("latin_1").decode("utf-8")


def _add_word_count(index, word):
    "Adds 1 to count and returns the index"
    if word in stopwords:
        return index
    if word in index:
        index[word] += 1
    else:
        index[word] = 1
    return index


def people_word_count():
    """ person -->  word --> nr"""
    index = dict()
    for dir_name, subdirs, thread in os.walk(inbox_path):
        for fname in thread:
            path = "/".join([dir_name, fname])
            if not re.findall(".json", path):
                continue
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                if "messages" not in data:
                    continue
                for msg in data["messages"]:
                    if not "content" in msg:
                        continue
                    content = _decode(msg["content"])
                    name = _decode(msg["sender_name"])
                    for word in _words(content):
                        if name in index:
                            _add_word_count(index[name], word)
                        else:
                            index[name] = _add_word_count(dict(), word)
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
