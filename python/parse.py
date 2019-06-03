import json
import sys
import pdb
import csv

import utils
import datetime
# import combine
import numpy

# sys.stdout = open('output.txt', 'w')

FILENAME = "../../data/message-5-1.json"
MOCKED = "../../data/mocked-message.json"

FILENAME_BASE = "../../data/message-10-31.json"
FILENAME_EXTRA = "../../data/message-12-25.json"


def read_data(file_name=FILENAME):
    with open(file_name, "r") as read_file:
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
        if "content" in message:
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
            if count > 999999:
                return
            if message["sender_name"][0] == target and "content" in message:
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


def report_metadata(messages, freq, should_print=True, threshhold=0):
    """
    this prints out the metadata from the messages, frequency dictionary
    """

    filtered, ratio= filter_freq(freq, threshhold)

    print("message count: " + str(len(messages)))
    print("total unique words: " + str(len(freq)))
    print("unique words appearing > " \
        + str(threshhold) + " times: " + str(len(filtered)))
    print("ratio: " + str(ratio))
    pretty_print_freq(filtered)


def write_to_csv(messages):
    """
    prep csv for gcp auto ml
    """

    MAX_COUNT = 100
    success, fail = 0, 0
    with open('../conversation.csv', mode='w') as csv_file:
        conversation_csv = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for message in messages[::-1]:
            if "content" in message:
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


def write_time_and_person_to_csv(times, target=None):
    """
    prep spreadsheet for message distribution
    take a list of integers and generate a table
    V,J,W
    0,value,value
    1,value,value
    ...
    23,value,value
    """

    with open('../times.csv', mode='w') as csv_file:
        times_csv = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        if target:
            for i in range(len(times)):
                times_csv.writerow([str(i) + ":00", times[i][0], times[i][1]])
        else:
            for i in range(len(times)):
                times_csv.writerow([str(i) + ":00", times[i]])


def write_time_to_csv(times):
    """
    prep spreadsheet for message distribution
    take a list of integers and generate a table
    0,value
    1,value
    ...
    23,value
    also optional target
    """

    with open('../times.csv', mode='w') as csv_file:
        times_csv = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i in range(len(times)):
            times_csv.writerow([str(i) + ":00", times[i]])


def write_all_times_to_csv(times, isCombined=True):
    """
    write all the times by person by minute instead of hour
    no clustering
    """
    with open('../weekday_times.csv', mode='w') as csv_file:
        times_csv = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        word = "MTWHFSN"

        if isCombined:
            times_csv.writerow(["PST"] + [c for c in word])
        else:
            times_csv.writerow(["PST"] + [c + '-J' for c in word] + [c + '-W' for c in word])

        for i in range(len(times)):
            times_csv.writerow([str(i) + ":00"] + times[i])


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


def hour_cluster(messages, target=None):
    """
    create 24 buckets and count the messages in each one
    hour is the index in the list
    returns a 24 element list
    optional filter
    when there's a filter - create a list of tuples
    first column is the target
    """
    if target:
        buckets = [[0, 0] for _ in range(24)]
    else:
        buckets = [0 for _ in range(24)]

    for message in messages:
        time = utils.get_time(message)
        hour = time.hour
        if not target:
            buckets[hour] += 1
        elif target == message["sender_name"][0]:
            buckets[hour][0] += 1
        else:
            buckets[hour][1] += 1
    return buckets


def week_hour_cluster(messages, target=None):
    """
    hour maps to 2 lists by days of the week
        M  T  W  H  F  S  N  M  T  W  H  F  S  N
    H, [#, #, #, #, #, #, #, #, #, #, #, #, #, #]
    combine if no target
    """
    if target:
        buckets = [[0 for _ in range(14)] for _ in range(24)]
    else:
        buckets = [[0 for _ in range(7)] for _ in range(24)]
    for message in messages:
        time = utils.get_time(message)
        hour = time.hour
        day = time.weekday()
        if not target or target == message["sender_name"][0]:
            buckets[hour][day] += 1
        else:
            buckets[hour][7 + day] += 1
    return buckets


def count_suffix(frequencies, suffix='z'):
    """
    filter by the suffix
    return the new dictionary
    """
    filtered = {}
    for key, value in frequencies.items():
        if key[-1].lower() == suffix.lower():
            utils.dput(filtered, key, value)
    return filtered


def write_z_to_csv(freqs, labels):
    """
    [freq_one, freq_two]
    [let, let]
         L L
    word N M
    word N M
    """
    combined = {}
    for key, value in freqs[0].items():
        combined[key] = [value, 0]
    for key, value in freqs[1].items():
        if key in combined:
            combined[key] =  [combined[key][0], value]
        else:
            combined[key] = [0, value]

    keys = sorted(combined.keys(),key=lambda(x):-1 * sum(combined[x]))

    with open('../freq_z.csv', mode='w') as csv_file:
        freq_z_csv = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        freq_z_csv.writerow(["artZ", labels[0], labels[1], "Total"])

        count = 0
        for key in keys:
            try:
                freq_z_csv.writerow([key, combined[key][0], combined[key][1], combined[key][0] + combined[key][1]])
            except UnicodeEncodeError:
                print(key, count)
                count += 1


def calc_count_by_day(messages):
    """
    cut off the day at the lowest frequency
    get a list of days followed by number of messages
    also label each day with the day of the week

    list of tuples (can be zeros)
        (date object, count)
    date object is based on the first day
    hash in the form 07/07/18
    """
    counts = {}
    for msg in messages:
        timestamp = msg["timestamp_ms"]
        date = utils.to_day_shift(timestamp)
        formatted_date = date.strftime("%x")
        utils.dput(counts, formatted_date)

    sorted_keys = sorted(counts.keys())
    # for key in sorted_keys:
    #     print(key + " " + str(counts[key]))

    return [(key, counts[key]) for key in sorted_keys]


def write_all_count_by_day_to_csv(counts):
    """
    date | count
    simple 2 column
    """
    with open('../counts_by_day.csv', mode='w') as csv_file:
        counts_by_day_csv = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        counts_by_day_csv.writerow(["Day", "Total Message Count", "(cutoff 5:00am PST)"])

        for count in counts:
            counts_by_day_csv.writerow([count[0], count[1]])


def get_unique_messages(messages, target, other):
    """
    only include messages that are unique to one person
    two buckets (dictionaries)
    add tuples (message, [list time object formatted as string]))
    message keys (easy to search), values are the list of time objects
    target then non target

    the both set is for words used by both people ... might use this later
    """

    target_dict = dict()
    other_dict = dict()
    both_dict = dict()

    for msg in messages:
        content = msg["content"]
        sender = msg["sender_name"][0]
        time = utils.get_time(msg)

        if content in both_dict:
            both_dict[content].append((sender, time))
            continue

        # use references to the two buckets to avoid repeating code
        curr_bucket, other_bucket = None, None
        if sender == target:
            curr_bucket = target_dict
            other_bucket = other_dict
        else:
            curr_bucket = other_dict
            other_bucket = target_dict


        if (content in other_bucket):
            # flush the content out of the other_bucket
            # add it to the both set
            popped = other_bucket.pop(content)  # this is a list of times
            for popped_time in popped:
                utils.dput_list(both_dict, content, (other, popped_time))
            utils.dput_list(both_dict, content, (sender, time))
        else:
            # go ahead and add it to curr_bucket
            utils.dput_list(curr_bucket, content, time)

    return target_dict, other_dict, both_dict


def write_messages_to_csv(unique_msg_buckets, labels):
    """
    pretty print the buckets
    could do ...
    the first two buckets:
        key, count, (maybe time, time ... )
    last bucket (both)
        key, count J, count W
    sort the words

    but for now just list all the words, sets of 10
    """
    for i in range(2):
        words = unique_msg_buckets[i].keys()
        total = len(words)
        filename = '../' + labels[i] + '_unique_words.csv'
        with open(filename, mode='w') as csv_file:
            unique_words_csv = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            unique_words_csv.writerow(["unique words phrase", "count", "TOTAL: " + str(total), labels[i]])

            for i in range(total // 10):
                idx = 10 * i
                row = words[idx:idx+10]
                try:
                    unique_words_csv.writerow(row)
                except UnicodeEncodeError:
                    pass

place = 0

def print_day(goal_day, messages):
    """
    take an input day and print the conversation on that day
    place is the index we left off at
    the first call starts at the front because we inverted messages
    """
    global place

    curr = messages[place]
    curr_time = utils.get_time(curr)
    count_included = 0

    while curr_time < goal_day and place < len(messages):
        # print("continue" + str(curr_time))
        # keep going
        place += 1
        curr = messages[place]
        curr_time = utils.get_time(curr)

    while utils.date_equal(curr_time, goal_day):
        # print("same" + str(curr_time))
        fancy_print(curr)
        place += 1
        count_included += 1
        curr = messages[place]
        curr_time = utils.get_time(curr)

    print("included: " + str(count_included))

    # sanity check
    if curr_time > goal_day:
        print("current time past goal_day, we are done")
        if count_included == 0:
            print("should be october 9th?")
            pdb.set_trace()

    if count_included == 0:
        print("problem")
        pdb.set_trace()



def fancy_print(msg):
    """
    fancy print a msg
    """
    sender = msg["sender_name"][0]
    space = " " * 80 if sender == "W" else ""
    try:
        print(space + msg["content"])
    except UnicodeEncodeError:
        print("unicode error")

def demos(demo):
    """
    run something demoable lol
    everything is based on messages
    """
    messages = read_data()
    # messages = filter_data(read_data())
    # messages = combine.combine(FILENAME_BASE, FILENAME_EXTRA)

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

    elif demo == "freq_z":
        freq_one = calc_frequency(messages, "W")
        freq_two = calc_frequency(messages, "J")
        filtered_one = count_suffix(freq_one, "Z")
        filtered_two = count_suffix(freq_two, "Z")
        report_metadata(messages, filtered_one)
        report_metadata(messages, filtered_two)
        write_z_to_csv([filtered_one, filtered_two], ["W", "J"])

    elif demo == "time":
        times = hour_cluster(messages, "J")
        write_time_and_person_to_csv(times, "J")

    elif demo == "day":
        times = week_hour_cluster(messages)
        write_all_times_to_csv(times)

    elif demo == "lapse":
        count_by_day = calc_count_by_day(messages)
        print(count_by_day)
        write_all_count_by_day_to_csv(count_by_day)

    elif demo == "unique":
        unique_msg_buckets = get_unique_messages(messages, "J", "W")
        for bucket in unique_msg_buckets:
            print(str(len(bucket)) + '\n')
        keys = unique_msg_buckets[2].keys()

        combined = "============= \n"

        for key in keys:
            combined += key + "    "
        print(combined)
        write_messages_to_csv(unique_msg_buckets, ["J", "W"])

    elif demo == "day_input":
        # ask for an integer since 7,7

        input_delta = None
        if len(sys.argv) > 1:
            input_delta = int(sys.argv[1])
        else:
            input_delta = input("input number of days since (7, 7): ")

        day = datetime.datetime(2018, 7, 7) + datetime.timedelta(days=input_delta)
        divide = " " + "=" * 10 + " "
        print("\n\n" + divide * 3 + "\n\n")
        print(divide + " day: " + str(input_delta) + divide)
        print(divide + day.strftime("%A %b %d") + divide)
        inverted_messages = messages[::-1]

        ALL = False

        if ALL:
            final = datetime.datetime(2018, 12, 1)
            diff = datetime.timedelta(days=1)
            while day < final:
                print_day(day, inverted_messages)
                day += diff
        else:
            print_day(day, inverted_messages)

        print("\n\n" + divide * 3 + "\n\n")
        print(divide + " day: " + str(input_delta) + divide)
        print(divide + day.strftime("%A %b %d") + divide)

    elif demo == "stickers":
        print("stickers")
        sticker_freq = {}
        for message in messages:
            if "sticker" in message:
                sticker_uri = message["sticker"]["uri"]
                utils.dput(sticker_freq, sticker_uri)

        for sticker, counter in sorted(sticker_freq.items(), key=lambda(x): -1 *x[1]):
            print(str(counter) + '   ' + sticker)

    elif demo == "timestamps":
        messages = messages[::-1]
        options = ['WW', 'WJ', 'JJ', 'JW']
        freq = {}
        all_deltas = {}
        for i in range(len(messages) - 1):
            message_one, message_two = messages[i], messages[i+1]
            time_one = utils.get_time(message_one)
            time_two = utils.get_time(message_two)
            time_diff = (time_two - time_one).seconds
            label = utils.get_sender(message_one)  + utils.get_sender(message_two)
            utils.dput_list(all_deltas, label, time_diff)
            key = (label, time_diff)
            utils.dput(freq, key)

        full_results = []
        MAX_SECONDS = 24 * 3600
        cutoffs = [5, 10, 30, 60, 300, 600, 1800, 3600, MAX_SECONDS]
        results = [0 for _ in range(4)]
        for delta in range(MAX_SECONDS + 1):
            curr_results = []
            for option in options:
                lookup = (option, delta)
                if lookup in freq:
                    count = freq[lookup]
                    curr_results += [count]
                else:
                    curr_results += [0]

            #combine curr_results with the other ones before the cutoff
            results = [curr_results[i] + results[i] for i in range(len(results))]

            if delta in cutoffs:
                results = [delta] + results
                full_results += [results]
                results = [0 for _ in range(4)]


        with open('../deltas.csv', mode='w') as csv_file:
            conversation_csv = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            conversation_csv.writerow([''] + options)
            for result in full_results:
                conversation_csv.writerow(result)

            for key in options:
                deltas = all_deltas[key]
                mean = numpy.mean(deltas)
                std = numpy.std(deltas)
                print(key + " | " + str(mean) + " | " + str(std))
                conversation_csv.writerow(['', "mean", "std"])
                conversation_csv.writerow([key, str(mean), str(std)])

        pdb.set_trace()




if __name__== "__main__":
    demos("timestamps")
