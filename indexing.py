import os
import json
from stop_words import get_stop_words
import regex as re
from datetime import date
import numpy as np

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
    else:
        return count(index, word)


def count(index, obj):
    if obj in index:
        index[obj] += 1
    else:
        index[obj] = 1
    return index


def people_word_count():
    """ person -->  word --> nr"""
    index = {}
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


def people_timestamp(self_name):
    """ Returns a dict with names as keys
        and a list of timestamps as values
        on the format [[recived_timestamp], [sent_timestamp]]. """
    index = {}
    for dir_name, subdirs, thread in os.walk(inbox_path):
        for fname in thread:
            path = "/".join([dir_name, fname])
            if not re.findall(".json", path):
                continue
            with open(path, encoding="utf-8") as f:
                thread = json.load(f)
                if "messages" not in thread or len(thread["participants"]) != 2:
                    continue
                participant1 = _decode(thread["participants"][0]["name"])
                participant2 = _decode(thread["participants"][1]["name"])
                if participant1 == self_name:
                    friend_name = participant2
                else:
                    friend_name = participant1
                if friend_name not in index:
                    index[friend_name] = [[], []]
                for msg in thread["messages"]:
                    if not "content" in msg:
                        continue
                    time = msg["timestamp_ms"]/1000
                    if msg["sender_name"] == friend_name:
                        index[friend_name][0].append(time)
                    else:
                        index[friend_name][1].append(time)
    return index


def msgs_per_day(people_timestamp_dict):
    ptd = people_timestamp_dict
    index = {}
    for name in ptd.keys():
        date_dict = {}
        [count(date_dict, date.fromtimestamp(ts)) for ts in ptd[name][0]]
        [count(date_dict, date.fromtimestamp(ts)) for ts in ptd[name][1]]
        index[name] = date_dict
    return index
