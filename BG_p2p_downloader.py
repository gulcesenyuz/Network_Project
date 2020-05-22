import socket
import json
import shutil
import os
import sys
from datetime import *

m_dic = {}


def has_key(f_n):
    if not f_n in m_dic:
        return False

    return True


def search(f_n, rec_ip, rec_un):
    if not f_n in m_dic:
        return False

    flag = False
    for y in m_dic[f_n]:
        if y["ip"] == rec_ip and rec_un == y["username"]:
            flag = True

    return flag


def combine_chunks(inp, s_dir, o_dir):
    if not os.path.exists(o_dir):
        os.makedirs(o_dir)
    with open(o_dir + '/' + inp, 'wb') as outfile:
        for i in range(1, 6):
            with open(s_dir + '/' + inp + "_" + str(i), "rb") as infile:
                outfile.write(infile.read())
    for i in range(1, 6):
        if os.path.exists(inp + "_" + str(i)):
            shutil.move(os.path.join(s_dir, inp + "_" + str(i)), "temp")
            os.remove(os.path.join(s_dir, inp + "_" + str(i)))
    print("Download finished. Check \'downloads\' folder for \'" + str(inp) + "\'.\n")


def main():
    tags_file = open("tags.txt", "r")
    json_data = tags_file.read()
    f_dic = {}
    try:
        f_dic = json.loads(json_data)
    except:
        print("empty tags.txt")
    for x in f_dic:
        for y in f_dic[x]:
            if not x[:-2] in m_dic:
                m_dic[x[:-2]] = [y]
            else:
                if not search(x[:-2], y["ip"], y["username"]):
                    m_dic[x[:-2]].insert(0, y)
    tags_file.close()

    for x in m_dic:
        for y in m_dic[x]:
            print("File Name: " + x + ", IP Address: " + y["ip"] + ", Client Tag: " + y["username"])
    selection = input("\nEnter the filename to download or Q(uit) or R(efresh): ")
    if selection.upper() == "R":
        print("\n")
        return
    if selection.upper() == "Q":
        print("\nClosing downloader. Bye!")
        sys.exit()
    for i in range(1, 6):
        if selection in m_dic:
            for x in m_dic[selection]:
                if p2p_client_start(selection + '_' + str(i), x["ip"]):
                    break
        else:
            print("\nNo file found available with this name. Please try again.\n")
            return
    combine_chunks(selection, "temp", "downloads")


def logger(message):
    log = open("client.log", "a")
    log.write(str(datetime.now()) + ': ' + message + "\n")
    log.close()


def p2p_client_start(f_n, ip):
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((ip, 5001))
    try:
        connection.send(json.dumps({"filename": f_n}).encode())
        chunks = open(os.path.join("temp", f_n), "wb")
        while True:
            data = connection.recv(2048)
            chunks.write(data)
            if len(data) == 0:
                print("Download of \'" + f_n + "\' from " + ip + " is successful.")
                logger("Download of \'" + f_n + "\' from " + ip + " is successful.")
                break
        return True
    except:
        print("Download of \'" + f_n + "\' from " + ip + " is unsuccessful. (!)")
        logger("Download of \'" + f_n + "\' from " + ip + " is unsuccessful. (!)")
        return False
    finally:
        connection.close()


if __name__ == '__main__':
    if not os.path.exists("tags.txt"):
        open("tags.txt", "w").close()

    if not os.path.exists("temp"):
        os.makedirs("temp")

try:
    while True:
        main()
except KeyboardInterrupt:
    print("\nClosing downloader. Bye!")
