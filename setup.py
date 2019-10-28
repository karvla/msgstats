import os 
import sys
import indexing
import pickle
import tf_idf_tools as tf_idf

path_home = os.path.expanduser('~')
path_config = path_home + '/.config'
path_msgstats = path_home + '/.config/msgstats'
path_cache = path_home + '/.config/msgstats/cache'
cache_file_name = "cache"

if __name__ == "__main__":
    print("Setting up folders..")
    try:
        os.makedirs(path_config)
        print("    " + path_config + " created")
    except OSError:
        print("    " + path_config + " skipped")
        
    try:
        os.makedirs(path_msgstats)
        print("    " + path_msgstats + " created")
    except OSError:
        print("    " +  path_msgstats + " skipped")

    messages_path = input("Path of 'messages/' folder: ")
    while True:
        try:
            os.listdir(messages_path + "/messages/")
            break
        except:
            pass
            print("    Error: " + messages_path + "/messages could not be found")
            messages_path = input("Path of 'messages/' folder: ")

    inbox_path = messages_path + "messages/inbox"
    self_name = input("Name (used on Facebook) of the data owner: ")


    print("Indexing files, pls wait ", end='')
     
    b = '\u2588'
    sys.stdout.write("[%s]" % (" " * 6))
    sys.stdout.write("\b" * (6 +1))
    sys.stdout.flush()

    pwc = indexing.people_word_count(inbox_path)
    sys.stdout.write(b)
    sys.stdout.flush()

    wpc = indexing.word_people_count(pwc)
    sys.stdout.write(b)
    sys.stdout.flush()

    pti = tf_idf.person_tf_idf(pwc, wpc)
    sys.stdout.write(b)
    sys.stdout.flush()

    pts = indexing.people_timestamp(self_name, inbox_path)
    sys.stdout.write(b)
    sys.stdout.flush()

    mpd = indexing.msgs_per_day(pts)
    sys.stdout.write(b)
    sys.stdout.flush()

    wpd = indexing.words_per_day(pts)
    sys.stdout.write(b)
    sys.stdout.flush()

    index = (pwc, wpc, pti, pts, mpd, wpd)
    os.chdir(path_msgstats)
    with open(cache_file_name, "wb") as f:
        pickle.dump(index, f)
    sys.stdout.write("]\n")
    sys.stdout.flush()

    print("Setup done!")

