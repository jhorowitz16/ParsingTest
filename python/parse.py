import json


def read_data():
    with open("../../data/message.json", "r") as read_file:
        data = json.load(read_file)
        return data["messages"]


def print_messages(messages, target):
    """
    print messages that were sent by a person (by target letter)
    """
    count = 0
    for message in messages[::-1]:
        if message["sender_name"][0] == target:
            print(message["content"])
            count += 1
    print(count)


def calc_frequency(messages):
    """
    return a frequency dictionary based on the list of messages
    do not include empty strings
    """
    freq = {}
    for message in messages:
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

    ratio = len(filtered) / len(freq)
    return filtered, ratio


def pretty_print_freq(freq):
    """
    print with extra spaces a word frequency table
    crop strings that are too long, and add spaces for short ones
    """

    TARGET = 10

    print("================================")
    for word, value in sorted(freq.items(), key=lambda(x): -1 *x[1]):
        n = len(word)
        if n <= TARGET:
            print(word + ' ' * (TARGET - n) + " | " + str(value))
    print("================================")


if __name__== "__main__":
    print("begin parsing")
    data = read_data()
    freq = calc_frequency(data)
    filtered, ratio = filter_freq(freq, 50)

    print(filtered)
    print("ratio: " + str(ratio))

    pretty_print_freq(filtered)
