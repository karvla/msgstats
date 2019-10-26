import regex as re
import pickle
from datetime import timedelta, datetime, date
import indexing
import matplotlib.pyplot as plt
from setup import path_cache, path_home
import os
import argparse

with open(path_cache, 'rb') as f:
    pwc, wpc, pti, pts, mpd, wpd = pickle.load(f)

def print_names_with_most_words_written(N=20):
    name_word_sum = [(name, sum(pwc[name].values())) for name in pwc.keys()]
    print("Most words written:")
    for i in sorted(name_word_sum, key=lambda x: x[1], reverse=True)[:N]:
        print(i)


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
    plt.show()


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

    parser = argparse.ArgumentParser(
        description="Tools for displaying stats on chat history."
    )
    parser.add_argument(
        "-fm",
        "--freq-messages",
        dest="f",
        action="store_const",
        const=lambda x: plot_freq(x , mpd),
        default=lambda x: x,
        help="plots the 30 days rolling averge of number of messages sent and received to/from the names given",
    )

    parser.add_argument(
        "-fw",
        "--freq-words",
        dest="f",
        action="store_const",
        const=lambda x: plot_freq(x , wpd),
        default=lambda x: x, 
        help="plots the 30 days rolling averge of number of words sent and received to/from the names given",
    )

    parser.add_argument(
        "-c",
        "--conversation",
        dest="f",
        action="store_const",
        const=lambda x: print_conv(x[0]),
        default=lambda x: x, 
        help="displays the conversation between two dates for a given name",
    )

    parser.add_argument(
            "-n",
            "--names",
            type=str,
            nargs="+",
            help = "names for persons separated by ',' "
    )


    parser.add_argument(
            "-d",
            "--date",
            type=lambda s: datetime.strptime(s, '%Y-%m-%d'),
            nargs=2,
            help = "names for persons separated by ',' "
    )


    args = parser.parse_args()
    names_list = " ".join(args.names).split(", ")
    args.f(names_list)
