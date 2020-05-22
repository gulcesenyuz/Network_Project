import json
import os
import time
import platform
from socket import *

h_ip = "25.72.129.89"


file_dic = {}


def has_key(f_n):
    if not f_n in file_dic:
        return False
    return True


def search(f_n, rec_ip, rec_un):
    if not f_n in file_dic:
        return False
    flag = False
    for ip, username in file_dic[f_n]:
        if rec_ip == ip and rec_un == username:
            flag = True
    return flag


def service_listener():
    connection = socket(AF_INET, SOCK_DGRAM)
    connection.bind(('25.255.255.255' if platform.system() != 'Windows' else h_ip, 5000))
    print("Listening for available files:\n")
    while True:
        msg, addr = connection.recvfrom(1024)
        ip = addr[0]
        print("Available client found at: " + ip)
        json_data = json.loads(msg.decode())
        f = json_data["files"]
        un = json_data["username"]
        for file in f:
            if search(file, ip, un):
                continue
            if has_key(file):
                file_dic[file].insert(0, {"username": un, "ip": ip})
            else:
                file_dic[file] = [{"username": un, "ip": ip}]
        tags_file = open("tags.txt", "w")
        tags_file.write(json.dumps(file_dic))
        tags_file.close()


if __name__ == '__main__':
    try:
        while not os.path.exists("tags.txt"):
            print("Download client is not started. Please run the p2p_downloader.py file.\n")
            time.sleep(10)

        l_u = open("tags.txt", "r")
        try:
            file_dic = json.loads(l_u.read())
        except:
            print("tags.txt is empty")
        service_listener()
    except KeyboardInterrupt:
        print("\nClosing listener service. Bye!")
