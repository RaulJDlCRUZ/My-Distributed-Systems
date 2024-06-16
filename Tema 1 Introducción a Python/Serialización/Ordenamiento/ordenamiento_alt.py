import struct
# Detectar el orden de los bytes con struct, según el empaquetado con un entero de 16 bits sin signo
print("big endian") if struct.pack('H', 1) == b'\x00\x01' else print("little endian")
