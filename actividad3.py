import pyshark
import argparse
import os


def hex_to_ascii(hex_string):
    """Convierte una cadena hexadecimal a una cadena de caracteres ASCII."""
    try:
        # Convierte la cadena hexadecimal a bytes
        bytes_object = bytes.fromhex(hex_string)
        # Decodifica los bytes a una cadena ASCII
        ascii_string = bytes_object.decode('ascii', errors='ignore')
        return ascii_string
    except ValueError:
        return ''


def caesar_cipher(text, shift):
    """Desplaza el texto cifrado con un cifrado César."""
    decrypted_text = []
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            start = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr(start + (ord(char) - start - shift_amount) % 26)
            decrypted_text.append(decrypted_char)
        else:
            decrypted_text.append(char)
    return ''.join(decrypted_text)


def main(file_path):
    # Cargar el archivo de captura
    cap = pyshark.FileCapture(file_path)

    # Inicializar una lista para almacenar los dos primeros caracteres de la data
    data_list = []

    # Iterar sobre los paquetes y almacenar solo los dos primeros caracteres de la data para ICMP con destino 8.8.8.8
    for packet in cap:
        if 'ICMP' in packet and hasattr(packet, 'ip') and packet.ip.dst == '8.8.8.8':
            if hasattr(packet.icmp, 'data') and packet.icmp.data:
                data = packet.icmp.data
                # Guardar los dos primeros caracteres en la lista
                data_list.append(data[:2])

    # Convertir y concatenar los datos guardados
    ascii_result = ''.join(hex_to_ascii(hex_value) for hex_value in data_list)

    # Mostrar todas las posibles palabras después de aplicar todos los desplazamientos posibles
    for shift in range(1, 26):
        decrypted_text = caesar_cipher(ascii_result, shift)
        print(f'{decrypted_text}')

    # Cerrar la captura
    cap.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Leer un archivo de captura de Wireshark.')
    parser.add_argument('file_path', type=str, help='Ruta al archivo de captura (.pcap)')

    args = parser.parse_args()

    # Construir la ruta completa
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, args.file_path)

    main(full_path)
