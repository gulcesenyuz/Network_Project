import os
from os.path import isfile, join
from socket import *
import time
import json
from os import listdir

path = "temp"


def announcer_start(tag):
    connection = socket(AF_INET, SOCK_DGRAM)
    connection.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    connection.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    count: int = 1

    while True:
        files = []
        for file in listdir(path):
            if isfile(join(path, file)):
                files.insert(0, file)
        message = json.dumps({"username": tag, "files": files})
        connection.sendto(message.encode(), ("25.255.255.255", 5000))
        print("[" + str(count) + "] Sending: " + str(message))
        count = count + 1
        time.sleep(60)


if __name__ == '__main__':
    try:
        if not os.path.exists("temp"):
            os.makedirs("temp")
        un = input("Enter your client tag: ")
        announcer_start(un)
    except KeyboardInterrupt:
        print("\nClosing announcer service. Bye!")
