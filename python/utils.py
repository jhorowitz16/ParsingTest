
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
