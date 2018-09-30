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
    """
    freq_dict = {}
    for message in messages:
        words = message["content"].split(" ")
        for word in words:
            if word in freq_dict:
                freq_dict[word] += 1
            else:
                freq_dict[word] = 1
    return freq_dict


if __name__== "__main__":
    print("begin parsing")
    data = read_data()
    print_messages(data, 'J')
    print_messages(data, 'W')
    freq_dict = calc_frequency(data)
    print(freq_dict)
