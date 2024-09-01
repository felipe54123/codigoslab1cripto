import sys

def cifrar_cesar(mensaje, corrimiento):
    resultado = []
    
    for char in mensaje:
        if char.isalpha():
            # Determinar el rango del alfabeto (mayúsculas o minúsculas)
            base = ord('A') if char.isupper() else ord('a')
            # Aplicar el corrimiento y envolver si es necesario
            nuevo_char = chr((ord(char) - base + corrimiento) % 26 + base)
            resultado.append(nuevo_char)
        else:
            # Mantener los caracteres no alfabéticos sin cambios
            resultado.append(char)
    
    return ''.join(resultado)

def main():
    #Control de errores para que se ejecute bien el programa    
    if len(sys.argv) != 3:
        print("Uso: python actividad1.py <mensaje> <corrimiento>")
        sys.exit(1)
    
    mensaje = sys.argv[1]
    try:
        corrimiento = int(sys.argv[2])
    except ValueError:
        print("El corrimiento debe ser un número entero.")
        sys.exit(1)
    
    mensaje_cifrado = cifrar_cesar(mensaje, corrimiento)
    print(mensaje_cifrado)

if __name__ == "__main__":
    main()
