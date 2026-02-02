import struct
import socket
import time
import sys
import os
import ast
import math
import json
import re



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

host = "127.0.0.1"
port = 9000

crc8_table = [
    0x00, 0x31, 0x62, 0x53, 0xC4, 0xF5, 0xA6, 0x97, 0xB9, 0x88, 0xDB, 0xEA, 0x7D, 0x4C, 0x1F, 0x2E,
    0x43, 0x72, 0x21, 0x10, 0x87, 0xB6, 0xE5, 0xD4, 0xFA, 0xCB, 0x98, 0xA9, 0x3E, 0x0F, 0x5C, 0x6D,
    0x86, 0xB7, 0xE4, 0xD5, 0x42, 0x73, 0x20, 0x11, 0x3F, 0x0E, 0x5D, 0x6C, 0xFB, 0xCA, 0x99, 0xA8,
    0xC5, 0xF4, 0xA7, 0x96, 0x01, 0x30, 0x63, 0x52, 0x7C, 0x4D, 0x1E, 0x2F, 0xB8, 0x89, 0xDA, 0xEB,
    0x3D, 0x0C, 0x5F, 0x6E, 0xF9, 0xC8, 0x9B, 0xAA, 0x84, 0xB5, 0xE6, 0xD7, 0x40, 0x71, 0x22, 0x13,
    0x7E, 0x4F, 0x1C, 0x2D, 0xBA, 0x8B, 0xD8, 0xE9, 0xC7, 0xF6, 0xA5, 0x94, 0x03, 0x32, 0x61, 0x50,
    0xBB, 0x8A, 0xD9, 0xE8, 0x7F, 0x4E, 0x1D, 0x2C, 0x02, 0x33, 0x60, 0x51, 0xC6, 0xF7, 0xA4, 0x95,
    0xF8, 0xC9, 0x9A, 0xAB, 0x3C, 0x0D, 0x5E, 0x6F, 0x41, 0x70, 0x23, 0x12, 0x85, 0xB4, 0xE7, 0xD6,
    0x7A, 0x4B, 0x18, 0x29, 0xBE, 0x8F, 0xDC, 0xED, 0xC3, 0xF2, 0xA1, 0x90, 0x07, 0x36, 0x65, 0x54,
    0x39, 0x08, 0x5B, 0x6A, 0xFD, 0xCC, 0x9F, 0xAE, 0x80, 0xB1, 0xE2, 0xD3, 0x44, 0x75, 0x26, 0x17,
    0xFC, 0xCD, 0x9E, 0xAF, 0x38, 0x09, 0x5A, 0x6B, 0x45, 0x74, 0x27, 0x16, 0x81, 0xB0, 0xE3, 0xD2,
    0xBF, 0x8E, 0xDD, 0xEC, 0x7B, 0x4A, 0x19, 0x28, 0x06, 0x37, 0x64, 0x55, 0xC2, 0xF3, 0xA0, 0x91,
    0x47, 0x76, 0x25, 0x14, 0x83, 0xB2, 0xE1, 0xD0, 0xFE, 0xCF, 0x9C, 0xAD, 0x3A, 0x0B, 0x58, 0x69,
    0x04, 0x35, 0x66, 0x57, 0xC0, 0xF1, 0xA2, 0x93, 0xBD, 0x8C, 0xDF, 0xEE, 0x79, 0x48, 0x1B, 0x2A,
    0xC1, 0xF0, 0xA3, 0x92, 0x05, 0x34, 0x67, 0x56, 0x78, 0x49, 0x1A, 0x2B, 0xBC, 0x8D, 0xDE, 0xEF,
    0x82, 0xB3, 0xE0, 0xD1, 0x46, 0x77, 0x24, 0x15, 0x3B, 0x0A, 0x59, 0x68, 0xFF, 0xCE, 0x9D, 0xAC
]


def crc8_calc(lp_block):
    """
    Вычисляет контрольную сумму CRC-8 для указанного набора данных.

    :param lp_block: последовательность байт (например, bytes или bytearray).
    :return: значение контрольной суммы типа unsigned char (байт).
    """
    # начальное значение контрольной суммы
    crc = 0xFF

    for b in lp_block:
        # применяем таблицу xor с текущим байтом и используем её значение
        crc = crc8_table[(crc ^ b)]

    return crc

def get_num(byte_data):
    byte_data.reverse()
    count = len(byte_data) - 1
    sum = 0
    for i in byte_data:
        sum += int(i) * math.pow(256, count)
        count -= 1

    return int(sum)


def xor_sum(buffer):
    # Начинаем с нулевого значения для накопителя результата
    temp_sum = 0

    # Проходим по каждому байту в переданном буфере
    for byte in buffer:
        # Применяем XOR текущего значения с очередным байтом
        temp_sum ^= byte

    # Возвращаем итоговую сумму
    return temp_sum


def get_bit(arr_byte):
    """
    Обрабатывает массив с байтами и возвращает биты в виде строки
    :param arr_byte: массив с байтами
    :return: возвращает строку с битами
    """

    bit_value = str()
    for iii in arr_byte:
        bit_value += f"{iii:08b}"

    return bit_value


def get_head(arr_byte):
    """

    :param arr_byte: массив с байтами заголовка
    :return: preamble: преамбула
    IDr: идентификатор получателя
    IDs: идентификатор отправителя
    byte_data: количество байт данных
    CSd: Контрольная сумма данных
    CSp: Контрольная сумма заголовка
    """

    preamble = "".join([chr(data[i]) for i in range(0, 4)])

    IDr = get_num([data[i] for i in range(4, 8)])

    IDs = get_num([data[i] for i in range(8, 12)])

    byte_data = get_num([data[i] for i in range(12, 14)])

    CSd = data[14]
    CSp = data[15]

    return preamble, IDr, IDs, byte_data, CSd, CSp


def binary_to_float(binary_string):
    # Преобразование двоичной строки в целое число
    integer_representation = int(binary_string, 2)

    # Упаковка целого числа в байтовый массив и распаковка его как float
    bytes_array = struct.pack('>I', integer_representation)
    float_value = struct.unpack('>f', bytes_array)[0]

    return float_value



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()

    conn, addr = s.accept()

    print("Connected by", addr)

    res = list()

    while True:
        data = conn.recv(1024)
        print(data)
        if chr(data[0]) == "@":
            if chr(data[18]) == "S":
                head = [data[i] for i in range(0, 15)]
                preamble, IDr, IDs, byte_data, CSd, CSp = get_head(head)

                IMEI_pref = "".join([chr(data[i]) for i in range(16, 20)])

                IMEI_list = [data[i] for i in range(20, len(data))]
                IMEI = "".join([chr(i) for i in IMEI_list])

                print(preamble, IDr, IDs, byte_data, CSd, CSp, IMEI_pref, IMEI)

                # Отправка ответа для авторизации
                res = bytearray()

                for i in "@NTC":
                    res.append(ord(i))

                # Количество занимаемых байт идентификатором получателем и отправителем равна по 4
                for i in IDs.to_bytes(length=4, byteorder="little"):
                    res.append(i)
                for i in IDr.to_bytes(length=4, byteorder="little"):
                    res.append(i)

                # Количество байт данных после заголовка(После 16 байта)(*<S)
                res.append(3)
                res.append(0)


                CSd = bytearray(int(i, 16) for i in "2a 3c 53".split(" "))
                CSd_sum = xor_sum(CSd)
                res.append(CSd_sum)
                CSp_sum = xor_sum(res)

                res.append(CSp_sum)

                for i in "2a 3c 53".split(" "):
                    res.append(int(i, 16))


                conn.send(res)

            elif chr(data[18]) == "F":
                head = [data[i] for i in range(0, 15)]
                preamble, IDr, IDs, byte_data, CSd, CSp = get_head(head)

                protocol = "".join([chr(data[i]) for i in range(16, 22)])

                sign_protocol = data[22]

                if sign_protocol == 176:
                    sign_protocol = "FLEX"

                protocol_version = data[23]
                struct_protocol = data[24]

                data_size = data[25]

                print(preamble, IDr, IDs, byte_data, CSd, CSp, protocol, sign_protocol, protocol_version, struct_protocol, data_size)

                enable_param_byte = dict()
                count = 1

                # Массив с битами, где 0 - выключена передача данных параметра, 1 - включена
                bit_enable_param = get_bit(data[26:])

                # json файл с данными по параметрам(Название, Количество занимаемых байт и тд)
                with open("Параметры.json", 'r') as file:
                    all_param = json.loads(file.read())

                # Запись в словарь какие параметры включены для передачи
                enable_param = dict()
                for i in range(1, len(bit_enable_param)):
                    if int(bit_enable_param[i-1]) == 1:
                        enable_param[i] = all_param[str(i)]

                # bitfield = data[26:]

                head = bytearray(int(i, 16) for i in "2a 3c 46 4c 45 58 b0 1e 1e".split(" "))
                res = bytearray()

                for i in preamble:
                    res.append(ord(i))

                for i in IDs.to_bytes(length=4, byteorder="little"):
                    res.append(i)
                for i in IDr.to_bytes(length=4, byteorder="little"):
                    res.append(i)

                # Байт данный после заголовка
                for i in len(head).to_bytes(length=2, byteorder="little"):
                    res.append(i)

                CSd_sum = xor_sum(head)
                res.append(CSd_sum)
                CSp_sum = xor_sum(res)

                res.append(CSp_sum)

                for i in head:
                    res.append(i)

                conn.send(res)

        elif chr(data[0]) == "~":
            preamble = "".join([chr(data[i]) for i in range(0, 3)])

            if chr(data[1]) == "T":
                eventindex = bytearray(data[i] for i in range(2, 6))

                telemat = bytearray(data[i] for i in range(6, len(data)-1))

                crc8 = data[-1]
                print(crc8)


                count = 0
                for i in enable_param:
                    enable_param[i]['Значение в байтах'] = [telemat[i] for i in range(count, count+enable_param[i]['Байт'])][::-1]
                    count += enable_param[i]['Байт']

                    for ii in enable_param[i]['Параметры']:
                        if enable_param[i]['Параметры'][ii]['Тип данных'] == "float":
                            value = binary_to_float(get_bit(enable_param[i]['Значение в байтах']))

                            enable_param[i]['Параметры'][ii]['Значение'] = round(value, 1)

                        elif enable_param[i]['Параметры'][ii]['Бит'] == "None" and enable_param[i]['Байт'] != 1:
                            if enable_param[i]['Параметры'][ii]['Тип данных'] == "int":
                                value = 0
                                count_pow = 1
                                for iii in enable_param[i]['Значение в байтах']:
                                    value +=  iii*math.pow(256, len(enable_param[i]['Значение в байтах'])-count_pow)
                                    count_pow += 1

                                enable_param[i]['Параметры'][ii]['Значение'] = int(value)
                        elif enable_param[i]['Параметры'][ii]['Бит'] == "None" and enable_param[i]['Байт'] == 1:
                                value = enable_param[i]['Значение в байтах'][0]

                                enable_param[i]['Параметры'][ii]['Значение'] = int(value)

                        # При условии, что в параметре всего один бит
                        elif len(enable_param[i]['Параметры'][ii]['Бит']) == 1 and enable_param[i]['Параметры'][ii]['Бит'] != "None":
                            if enable_param[i]['Параметры'][ii]['Тип данных'] == "bool":
                                bit = get_bit(enable_param[i]['Значение в байтах'])

                                value = bit[7-int(enable_param[i]['Параметры'][ii]['Бит'])]

                                enable_param[i]['Параметры'][ii]['Значение'] = int(value)

                        else:
                            if enable_param[i]['Параметры'][ii]['Бит'] != "None":
                                bit = get_bit(enable_param[i]['Значение в байтах'])

                                # value = bit[7 - int(enable_param[i]['Параметры'][ii]['Бит'])]
                                bit_temp = enable_param[i]['Параметры'][ii]['Бит'].split("-")
                                bit_st = int(bit_temp[0])
                                bit_end = int(bit_temp[1])
                                bit_order = [i for i in range(bit_st, bit_end+1)]

                                bit_str = str()
                                for iii in bit_order:
                                    bit_str += bit[7-iii]

                                value = 0

                                count_pow = 1
                                for iii in bit_str[::-1]:
                                    value += int(iii)*math.pow(2, len(bit_str)-count_pow)
                                    count_pow += 1
                                enable_param[i]['Параметры'][ii]['Значение'] = int(value)


                for i in enable_param:
                    for ii in enable_param[i]['Параметры']:
                        print(f"{enable_param[i]['Параметры'][ii]['Название']}: {enable_param[i]['Параметры'][ii]['Значение']}, Байт - {enable_param[i]['Байт']}")

                res = bytearray()
                # ~T
                for i in "7e 54".split(" "):
                    res.append(int(i, 16))

                # eventindex
                for i in eventindex:
                    res.append(i)

                res.append(crc8_calc(res))

                conn.send(res)


        print()
        time.sleep(0.5)

