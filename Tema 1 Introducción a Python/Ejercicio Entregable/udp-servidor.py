#!/usr/bin/python3
# Bosquejo de servidor propuesto por Paula Castillejo Bravo

import socket
import random
import struct
import time

server_addr = ('', 4080)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind(server_addr)
    alunado = dict([("", "NULL")])

    while 1:
        print('Waiting for messages...')
        # Recibir alumno
        msg, addr = s.recvfrom(1024)
        msg = msg.decode('utf-8', 'replace')

        if msg[:3] == "UID":
            # Enviar colores al cliente Funcion
            colorBase = (['rojo', 'naranja', 'amarillo', 'verde',
                         'azul', 'morado', 'blanco', 'negro'])
            color = random.choice(colorBase).encode()
            l = len(color)
            format = f'!f{str(l)}silh'
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            hour = current_time[:2]
            minute = current_time[3:5]
            second = current_time[6:8]
            data = struct.pack(format, len(color), color,
                               int(hour), int(minute), int(second))
            s.sendto(data[0:], addr)
            Alumno = msg[3:]
            print('Sending messanger to ' + Alumno + '...')
            colorDec = color.decode()
            alunado[Alumno] = f"{Alumno}"
            alunado[colorDec] = f"{colorDec}"
            alunado[hour] = f"{hour}"
            alunado[minute] = f"{minute}"

        # Comprobar respuesta
        if msg[:3] == 'RES':
            espacio = msg.split(' ')
            tiempo = espacio[1].split(':')
            horaT = tiempo[0]
            minuteT = tiempo[1]
            colorT = msg[3:-9]

            print(alunado)

            if Alumno == alunado[f'{Alumno}'] and horaT == alunado[f"{horaT}"] and minuteT == alunado[f"{minuteT}"] and colorT == alunado[f"{colorT}"]:
                # Confirmar respuesta
                s.sendto('OK.'.encode(), addr)
                print(alunado[f'{Alumno}'] + ' has passed the test.')
            else:
                s.sendto('FAIL.'.encode(), addr)
