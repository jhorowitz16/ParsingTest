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
    return the messages
    """
    base_messages = parse.read_data(FILENAME_BASE)
    extra_messages = parse.read_data(FILENAME_EXTRA)

    final_base = base_messages[0]["timestamp_ms"]

    i = len(extra_messages) - 1
    extra = None
    while i > 0:
        extra = extra_messages[i]["timestamp_ms"]
        if extra == final_base:
            print("overlap timestamp:" + str(extra))
            break
        i -= 1

    x = extra_messages[:i]
    first = extra_messages[:i+1]
    all_messages = extra_messages[:i+1] + base_messages
    base, extra, overlap = len(base_messages), len(extra_messages), i
    total = len(all_messages)
    prev = all_messages[0]["timestamp_ms"]
    for msg in all_messages:
        curr = msg["timestamp_ms"]
        if curr - prev > 0:
            pdb.set_trace()
        prev = curr

    return all_messages


if __name__== "__main__":
    combine(FILENAME_BASE, FILENAME_EXTRA)
