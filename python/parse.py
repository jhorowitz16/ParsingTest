import json
import sys
import pdb

sys.stdout = open('output.txt', 'w')


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


if __name__== "__main__":
    messages = read_data()
    freq_one = calc_frequency(messages, "W")
    freq_two = calc_frequency(messages, "J")
    report_metadata(messages, freq_one)
    report_metadata(messages, freq_two)
