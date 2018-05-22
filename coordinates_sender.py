# -*- coding: utf-8 -*-
import time
import struct
import socket
HOST = 'localhost'
PORT = 38202


# Все данные запакованы в big endian.
for i in range(5):

    version_event_type = struct.pack('!B', 0x01) # версия протокола

    event_type = struct.pack('!B', 0x01) #  Отправка координат

    event_time = struct.pack('!I', int(time.time())) # время, unix timestamp, 4 байта

    latitude_local = 0.0
    longitude_local = 0.0
    latitude = struct.pack('!i', int(latitude_local * 10000000))# 4 байта широта
    longitude =struct.pack('!i', int(longitude_local * 10000000)) # 4 байта долгота

    elevation = struct.pack('!h', -267) # Высота над уровнем моря в метрах

    user_key = struct.pack('!8s', b'EyGeDCfJ') #bytes([0x00 ,0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]) # 8 байт ключа пользователя, полученные при авторизации

    data_packet = version_event_type + event_type + event_time + latitude + longitude + elevation + user_key
    # размер пакета 24 байта



    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(data_packet)
    header = s.recv(6) # В ответ 6+ байт
    print ('header: ', header)
    if header:
        recieved = header[0]
        urgency = header[1]
        msglen = struct.unpack('!I', header[2:6])[0]
        if msglen:
            message = s.recv(msglen)
            print("Message recieved:", message)

    


