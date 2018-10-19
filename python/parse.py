import json
import sys
import pdb
import csv

import utils
import datetime

# sys.stdout = open('output.txt', 'w')


def read_data():
    with open("../../data/message.json", "r") as read_file:
        data = json.load(read_file, encoding='utf-8')
        return data["messages"]

def filter_data(messages):
    """
    return a subset of messages that have the filterz
    """

    new_messages = []
    for msg in messages:
        try:
            filtered = utils.filter_msg(msg)
            if filtered:
                new_messages.append(filtered)
        except TypeError:
            print(msg)
            pdb.set_trace()
    return new_messages


def calc_frequency(messages, target):
    """
    return a frequency dictionary based on the list of messages
    do not include empty strings
    can filter by person (target letter starting the name)
    """
    freq = {}
    for message in messages:
        if target and message["sender_name"][0] != target:
            continue
        words = message["content"].split(" ")
        for word in words:
            if len(word) > 0:
                if word in freq:
                    freq[word] += 1
                else:
                    freq[word] = 1
    return freq


def print_messages(messages, target):
    """
    print messages that were sent by a person (by target letter)
    """
    count = 0
    for message in messages[::-1]:
        try:
            if count > 250:
                return
            if True or message["sender_name"][0] == target:
                print(str(count) + " " + message["sender_name"][0] + ": " + message["content"])
                count += 1
        except UnicodeEncodeError:
            word = "ENCODE ERROR"
            print("UNICODE-ERR | " + str(count))



def filter_freq(freq, thresh):
    """
    help format the frequency dictionary of words
    return a smaller set with a count >= thresh
    along with the ratio of shrinking
    """
    if len(freq) ==  0:
        return {}

    filtered = {}
    for key, val in freq.items():
        if val >= thresh:
            filtered[key] = val

    ratio = 1.0 * len(filtered) / len(freq)
    return filtered, ratio


def pretty_print_freq(freq):
    """
    print with extra spaces a word frequency table
    crop strings that are too long, and add spaces for short ones
    """

    TARGET = 11

    print("================================")
    for word, value in sorted(freq.items(), key=lambda(x): -1 *x[1]):
        n = len(word)
        if n <= TARGET:
            try:
                print(word + ' ' * (TARGET - n) + " | " + str(value))
            except UnicodeEncodeError:
                word = "ENCODE ERROR"
                print("UNICODE-ERR | " + str(value))

    print("================================")


def generate_word_cloud(freq):
    """
    get the format the wordcloud is looking for

    """
    pass


def report_metadata(messages, freq, should_print=True):
    """
    this prints out the metadata from the messages, frequency dictionary
    """

    THRESH = 200
    filtered, ratio= filter_freq(freq, 100)

    print("message count: " + str(len(messages)))
    print("total unique words: " + str(len(freq)))
    print("unique words appearing > " \
        + str(THRESH) + " times: " + str(len(filtered)))
    print("ratio: " + str(ratio))
    pretty_print_freq(filtered)


def write_to_csv(messages):
    """
    prep csv for gcp auto ml
    """

    MAX_COUNT = 100
    success, fail = 0, 0
    with open('conversation.csv', mode='w') as employee_file:
        conversation_csv = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for message in messages[::-1]:
            # if success > MAX_COUNT:
            #     return
            content = message["content"]
            sender_name = message["sender_name"][0]
            try:
                conversation_csv.writerow([content, sender_name])
                success += 1
            except:
                print("UNICODE-ERR")
                fail += 1
    print("success: " + str(success))
    print("fail: " + str(fail))


def calc_msg_lengths(messages, target):
    """
    understand the distribution of message lengths
    put everything in a dictionary
    make the keys the word lengths - and then map to a list of timestamps
    return two dictionaries for both people
    normalize
    """
    lengths_target, lengths_other = {}, {}
    for message in messages:
        content = message["content"]
        sender_name = message["sender_name"][0]
        if sender_name == target:
            utils.dput(lengths_target, len(content))
        else:
            utils.dput(lengths_other, len(content))
    return lengths_target, lengths_other


def text_based_histogram(keys, values, bucket_size, max_pound_signs,
    title='===='):
    """
    1 - 3  ##########
    4 - 6  ################
    ...
    starting with non-variable sized buckets (probably skewed)
    find the pound sign to bucket ratio based on the most frequent value
    key - the tuple 1st number to last number
    value - the number of pound signs
    then convert to strings - and pad the lengths
    assume bucket size 1 for now

    4 numbers bucket 2 --> 2 by 2
    5 numbers bucket 2 --> 2 by 2 then everything else

    add up all the values in the bucket
    normalize later
    """

    # setup
    histogram = {}
    bucket_vals = []

    for i in range((len(keys) - bucket_size) / bucket_size):
        idx = bucket_size * i
        bucket_val = 0
        for j in range(idx, idx + bucket_size):
            bucket_val += values[j]
        bucket_vals.append(bucket_val)

    # normalize so that the largest bucket has the max pound signs
    pound_ratio = 1.0 * max_pound_signs / max(bucket_vals)

    for i in range((len(keys) - bucket_size) / bucket_size):
        idx = bucket_size * i
        histogram[(keys[idx], keys[idx + bucket_size - 1])] = \
            1.0 * bucket_vals[i] * pound_ratio

    print(title)

    # print nonzero (3 digits)
    for key, val in sorted(histogram.items()):
        if int(val):
            pounds = '#' * int(val)
            key_str = ' ' * (3 - len(str(key[0]))) + str(key[0])
            key_str += ' to '
            key_str += ' ' * (3 - len(str(key[1]))) + str(key[1])
            print(key_str + " | " + pounds)


def hour_cluster(messages):
    """
    create 24 buckets and count the messages in each one
    hour is the index in the list
    returns a 24 element list

    """
    buckets = [0 for _ in range(24)]
    for message in messages:
        time = utils.get_time(message)
        hour = time.hour
        buckets[hour] += 1
    return buckets


def demos(demo):
    """
    run something demoable lol
    everything is based on messages
    """
    messages = filter_data(read_data())

    if demo == "histograms":
        word_lengths = calc_msg_lengths(messages, "J")
        text_based_histogram(word_lengths[0].keys(), word_lengths[0].values(), 5, 25, "============= J =============")
        text_based_histogram(word_lengths[1].keys(), word_lengths[1].values(), 5, 25, "============= W =============")

    elif demo == "print":
        print_messages(messages, "J")
        print_messages(messages, "W")

    elif demo == "frequencies":
        write_to_csv(messages)
        freq_one = calc_frequency(messages, "W")
        freq_two = calc_frequency(messages, "J")
        report_metadata(messages, freq_one)
        report_metadata(messages, freq_two)
        print_messages(messages, "W")

    elif demo == "time":
        print(hour_cluster(messages))




if __name__== "__main__":
    demos("time")
