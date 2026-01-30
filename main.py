import socket
import time
import sys
import os
import ast
import math

# response = "2a 3e 46 4c 45 58 b0 1e 1e"
# res = bytearray()
# for i in response.split(" "):
#     print(f"{format(int(i, 16), "x")}")
#     res.append(int(i, 16))
#
# print(res)
#
# print(response.replace(" ", ""))
# # print(ast.literal_eval(response.replace(" ", "")))
# quit()

host = "localhost"
port = 9000


def get_num(byte_data):
    byte_data.reverse()
    count = len(byte_data) - 1
    sum = 0
    for i in byte_data:
        sum += int(i) * math.pow(256, count)
        count -= 1

    return int(sum)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()

    conn, addr = s.accept()

    print("Connected by", addr)

    res = list()

    while True:
        data = conn.recv(1024)
        # with open("test.txt", "w") as file:
        #     file.write(str(data))
        # sys.stdout.write(f"{data}")
        res.append(data.hex())
        # print(data.decode("utf-8"))
        print(data.hex())
        print(data)
        print(len(data))
        if chr(data[0]) == "@":
            preamble = "".join([chr(data[i]) for i in range(0, 4)])

            IDr = get_num([data[i] for i in range(4, 8)])

            # IDr.reverse()
            # count = len(IDr)-1
            # sum = 0
            # for i in IDr:
            #     sum += int(i)*math.pow(256, count)
            #     count -= 1
            #
            # IDr = int(sum)

            IDs = get_num([data[i] for i in range(8, 12)])

            byte_data = get_num([data[i] for i in range(12, 14)])

            CSd = data[14]
            CSp = data[15]

            IMEI_pref = "".join([chr(data[i]) for i in range(16, 20)])

            IMEI_list = [data[i] for i in range(20, len(data))]
            IMEI = "".join([chr(i) for i in IMEI_list])
            print(chr(data[20]))

            print(preamble, IDr, IDs, byte_data, CSd, CSp, IMEI_pref, IMEI)




            # response = "2a 3e 46 4c 45 58 b0 1e 1e"
            res = bytearray()
            #
            for i in range(0, 16):
                res.append(0)
            #
            #
            # for i in response.split(" "):
            #     res.append(int(i, 16))
            #
            count = 0
            for i in "@NTC":
                res.insert(count, ord(i))
                count += 1

            for i in IDs.to_bytes(length=4, byteorder="little"):
                res.insert(count, i)
                count += 1
            for i in IDr.to_bytes(length=4, byteorder="little"):
                res.insert(count, i)
                count += 1

            for i in range(0, 2):
                # res.insert(count, 0)
                count += 1

            res.insert(count, CSd)
            count += 1
            res.insert(count, CSp)
            print(count)

            # print(IMEI_list)

            # for i in IMEI_list:
                # print(i)
                # print(int(i, 16))
                # res.append(i)
                # count += 1

            for i in "2a 3c 53".split(" "):
                res.append(int(i, 16))

            conn.send(res)

            print(res)
            #

            #
            # conn.send(res)
            # print(f"send - {res}")
            #
            # print(res)




            # for i in range(4, 35):
            #     if i<=3:
            #         print(chr(data[i]))

        # try:
        #     print(int(data.hex(), 16))
        # except Exception:
        #     pass
        print()
        # count = 0
        # for i in data:
        #     try:
        #         print(str(data[count]).hex())
        #     except AttributeError as e:
        #         print(data[count])
        #     count += 1
        # count = 1
        # for i in bytes(data):
        #     print(f"{count}: {i}")
        #     count += 1


        # time.sleep(0.5)

