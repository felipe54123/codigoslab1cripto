import sys
import random
import time
from binascii import unhexlify
from scapy.all import sr1, ICMP, IP

def unix_timestamp_bytes():
    # Obtener el timestamp UNIX actual
    timestamp = int(time.time())

    # Convertir el timestamp a bytes en formato little-endian (4 bytes)
    timestamp_bytes = timestamp.to_bytes(4, byteorder='little')

    return timestamp_bytes

def variable_bytes(char):
    # Agregar dos caracteres aleatorios al carácter proporcionado
    random_chars = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(2))
    variable = char + random_chars

    return variable.encode()

def tail_bytes():
    # Hex stream convertido en bytes
    tail_hex = "0000000000101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f3031323334353637"
    tail_bytes = unhexlify(tail_hex)

    return tail_bytes

def enviar_ping(ip_destino, identifier, sequence, letra):
    # Obtener los bytes para el payload según tus especificaciones
    timestamp_bytes = unix_timestamp_bytes()
    variable_bytes_value = variable_bytes(letra)
    tail_bytes_value = tail_bytes()

    # Componer el payload
    payload = timestamp_bytes + b"\x00\x00\x00\x00" + variable_bytes_value + tail_bytes_value

    # Crear un paquete ICMP (ping echo request) con los parámetros proporcionados y el payload
    paquete = IP(dst=ip_destino, ttl=64) / ICMP(id=identifier, seq=sequence) / payload

    # Enviar el paquete y esperar por una respuesta
    respuesta = sr1(paquete, verbose=False)

    if respuesta:
        print("Sent 1 packet")

def enviar_mensaje(mensaje):
    identifier = 11037
    sequence = 1

    for letra in mensaje:
        enviar_ping("8.8.8.8", identifier, sequence, letra)
        sequence += 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <mensaje>")
    else:
        mensaje = sys.argv[1]
        enviar_mensaje(mensaje)