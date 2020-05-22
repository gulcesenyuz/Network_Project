import json
from socket import *
from threading import *
from datetime import *
import os
import math
import platform

h_ip = "25.72.129.89"


def divide_into_chunks(f, direct):
    if not os.path.exists(direct):
        os.makedirs(direct)
    c: int = os.path.getsize(f)
    chunk_size = math.ceil(math.ceil(c) / 5)
    cnt = 1
    with open(f, 'rb') as infile:
        d_f = infile.read(int(chunk_size))
        while d_f:
            name = direct + "/" + f + "_" + str(cnt)
            with open(name, 'wb+') as div:
                div.write(d_f)
            cnt += 1
            d_f = infile.read(int(chunk_size))


def logger(message):
    log = open("server.log", "a")
    log.write(str(datetime.now()) + ': ' + message + "\n")
    log.close()


def server_start():
    connection = socket(AF_INET, SOCK_STREAM)
    connection.bind((h_ip, 5001))
    connection.listen(10)
    print("File is ready to send. Please make sure service_announcer.py file is running.\n")
    while True:
        con, info = connection.accept()
        Thread(target=execute, args=(con, info)).start()


def execute(con, info):
    the_file = ""
    suc = False
    while True:
        try:
            msg = con.recv(1024)
            if len(msg) == 0:
                break
            the_file = json.loads(msg.decode())["filename"]
            f = open("temp/" + the_file, "rb")
            con.send(f.read())
            f.close()
            suc = True
        except:
            suc = False
        finally:
            if suc:
                logger("Connection of \'" + the_file + "\' from " + str(info[0]) + " is successful.")
            con.close()


if __name__ == '__main__':
    flag = False
    while not flag:
        try:
            path = input("Enter the file's name: ")
            splitter = path.split('/' if platform.system() != 'Windows' else '\\')
            file = splitter[len(splitter) - 1]
            divide_into_chunks(file, "temp")
            server_start()
            Flag = True
        except KeyboardInterrupt:
            print("\nClosing server. Bye!")
            break
        except:
            print("\nAn unexpected error occurred. Please try again.\n")
            Flag = False
