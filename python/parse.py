import json
import sys
import pdb
import csv


# sys.stdout = open('output.txt', 'w')


def read_data():
    with open("../../data/message.json", "r") as read_file:
        data = json.load(read_file, encoding='utf-8')
        return data["messages"]


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
    with open('conversation.csv', mode='w') as employee_file:
        conversation_csv = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        success, fail = 0, 0
        for message in messages[::-1]:
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




if __name__== "__main__":
    messages = read_data()
    write_to_csv(messages)
    # freq_one = calc_frequency(messages, "W")
    # freq_two = calc_frequency(messages, "J")
    # report_metadata(messages, freq_one)
    # report_metadata(messages, freq_two)
    # print_messages(messages, "W")
