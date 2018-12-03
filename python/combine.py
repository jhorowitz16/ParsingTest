import sys
import parse
import pdb
import utils


FILENAME_BASE = "../../data/message-10-31.json"
FILENAME_EXTRA = "../../data/message-12-2.json"


def combine(base, extra):
    """
    read both files
    get the final timestamp on the first list
    find which message has that timestamp
    construct the combined version
    write to csv
    """
    print(base, extra)
    base_messages = parse.read_data(FILENAME_BASE)
    extra_messages = parse.read_data(FILENAME_EXTRA)

    final_base = base_messages[0]["timestamp_ms"]

    i = len(extra_messages) - 1
    extra = None
    while i > 0:
        extra = extra_messages[i]["timestamp_ms"]
        print(final_base - extra)
        if extra == final_base:
            print("overlap:" + str(extra))
            break
        i -= 1
    print(extra)





if __name__== "__main__":
    combine(FILENAME_BASE, FILENAME_EXTRA)
