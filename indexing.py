import os
import json
from stop_words import get_stop_words
import regex as re
from datetime import date
import tf_idt


def _words(text):
    return list(re.findall(r"\p{L}+", text.lower()))


def _decode(string):
    return string.encode("latin_1").decode("utf-8")


def _add_word_count(index, word):
    "Adds 1 to count and returns the index"
    stopwords = set((get_stop_words("en"))).union(
        set(get_stop_words("sv"))
    )  # TODO: Make not hardcoded
    if word in stopwords:
        return index
    else:
        return count(index, word)


def count(index, obj, N=1):
    if obj in index:
        index[obj] += N
    else:
        index[obj] = N
    return index


def people_word_count(inbox_path):
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


def people_timestamp(self_name, inbox_path):
    """ Returns a dict with names as keys
        and a list of timestamps as values on the format
        [[(recived_timestamp, n_words)], [(sent_timestamp, n_words)]]. """
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
                    index[friend_name] = {"from" : [], "to": []}
                for msg in thread["messages"]:
                    if not "content" in msg:
                        continue
                    content = _decode(msg["content"])
                    n_words = len(_words(content))
                    time = msg["timestamp_ms"]/1000
                    msg_dict = {"content": content, "n_words": n_words, "timestamp": time}
                    if _decode(msg["sender_name"]) == friend_name:
                        msg_dict["name"] = friend_name
                        index[friend_name]["from"].append(msg_dict)
                    else:
                        msg_dict["name"] = self_name
                        index[friend_name]["to"].append((msg_dict))
    return index


def msgs_per_day(people_timestamp_dict):
    ptd = people_timestamp_dict
    index = {}
    d = date.fromtimestamp
    for name in ptd.keys():
        date_recieved = {}
        date_sent = {}
        [count(date_recieved, d(msg["timestamp"])) for msg in ptd[name]["from"]]
        [count(date_sent, d(msg["timestamp"])) for msg in ptd[name]["to"]]
        index[name] = {"to": date_sent, "from": date_recieved}
    return index

def words_per_day(people_timestamp_dict):
    ptd = people_timestamp_dict
    index = {}
    d = date.fromtimestamp
    for name in ptd.keys():
        date_recieved = {}
        date_sent = {}
        [count(date_recieved, d(msg["timestamp"]), msg["n_words"]) for msg in ptd[name]["from"]]
        [count(date_sent, d(msg["timestamp"]), msg["n_words"]) for msg in ptd[name]["to"]]
        index[name] = {"to": date_sent, "from": date_recieved}
    return index

def person_tf_idt(person_word_count, word_person_count) -> dict:
    """ Returns a dict with a tf_idt-array for every person"""
    pwc = person_word_count
    wpc = word_person_count
    pti = dict()
    for name in pwc.keys():
        pti[name] = tf_idt.tf_idt_words(name, wpc, pwc)
    return pti




