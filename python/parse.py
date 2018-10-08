import json
import sys
import pdb
import csv

import utils

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
            new_messages.append(utils.filter_msg(msg))
        except TypeError:
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
            if count > 2500:
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


def text_based_histogram(keys, values, bucket_size, max_pound_signs):
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
    """

    most_frequent = max(values)
    pound_ratio = 1.0 * max_pound_signs / most_frequent
    histogram = {}

    for i in range(len(keys) / bucket_size):
        histogram[(keys[i], keys[i])] = \
            1.0 * values[i] * pound_ratio * max_pound_signs

    for key, val in sorted(histogram.items()):
        print(str(key) + " | " + str(val))


if __name__== "__main__":
    messages = read_data()
    messages = filter_data(messages)
    print_messages(messages, "J")
    # word_lengths = calc_msg_lengths(messages, "J")
    # print(word_lengths[0].keys())
    # print(word_lengths[1].keys())
    # text_based_histogram(word_lengths[0].keys(), word_lengths[0].values(), 1, 150)

    # write_to_csv(messages)
    # freq_one = calc_frequency(messages, "W")
    # freq_two = calc_frequency(messages, "J")
    # report_metadata(messages, freq_one)
    # report_metadata(messages, freq_two)
    # print_messages(messages, "W")
