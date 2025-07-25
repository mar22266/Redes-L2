# Andre Marroquin
import sys
import random

# CAPA DE APLICACIÓN
# solicitar_mensaje, mostrar_mensaje
def capa_aplicacion():
    mensaje = input("CAPA DE APLICACIÓN\nIngrese el mensaje (1 carácter): ").strip()
    if len(mensaje) != 1:
        raise ValueError("Debe ingresar exactamente un carácter.")
    print("Mensaje original:", mensaje)
    return mensaje

# CAPA DE PRESENTACIÓN
# codificar_mensaje, decodificar_mensaje
def capa_presentacion(mensaje: str):
    binario = format(ord(mensaje), '08b')
    print("\nCAPA DE PRESENTACIÓN")
    print("Mensaje en binario (ASCII):", binario)
    return binario

# CAPA DE ENLACE
# calcular_integridad, verificar_integridad, corregir_mensaje
def capa_enlace(data_bits: str, block_size: int):
    result = fletcher_checksum(data_bits, block_size)
    print("\nCAPA DE ENLACE")
    print("Mensaje con checksum (Fletcher):", result)
    return result

# CAPA DE RUIDO
# aplicar_ruido
def capa_ruido(trama: str):
    trama_lista = list(trama)
    index = random.randint(0, len(trama_lista) - 1)
    trama_lista[index] = '1' if trama_lista[index] == '0' else '0'
    corrupta = ''.join(trama_lista)
    print("\nCAPA DE RUIDO")
    print(f"Bit alterado en posición {index}")
    print("Trama con ruido:", corrupta)
    return corrupta

# CAPA DE TRANSMISIÓN
# enviar_informacion, recibir_informacion
def capa_transmision(trama: str):
    print("\nCAPA DE TRANSMISIÓN")
    print("Datos transmitidos (posiblemente corruptos):", trama)

# FUNCION CHECKSUM
def fletcher_checksum(data_bits: str, block_size: int) -> str:
    if block_size not in (8, 16, 32):
        raise ValueError("block_size debe ser 8, 16 o 32")
    
    length = len(data_bits)
    if length < block_size or (length % block_size != 0):
        pad_len = ((length + block_size - 1) // block_size) * block_size - length
        data_bits += '0' * pad_len

    mod = (1 << block_size) - 1
    sum1 = 0
    sum2 = 0
    for i in range(0, len(data_bits), block_size):
        word = int(data_bits[i:i+block_size], 2)
        sum1 = (sum1 + word) % mod
        sum2 = (sum2 + sum1) % mod

    chk1 = format(sum1, f'0{block_size}b')
    chk2 = format(sum2, f'0{block_size}b')
    return data_bits + chk1 + chk2

# FUNCION PRINCIPAL
def main():
    print("=== SIMULACIÓN DE TRANSMISIÓN CON MODELO OSI ===")
    try:
        block_size = int(input("Ingrese tamaño de bloque para checksum (8, 16 o 32): ").strip())
        
        mensaje = capa_aplicacion()
        binario = capa_presentacion(mensaje)
        con_checksum = capa_enlace(binario, block_size)
        con_ruido = capa_ruido(con_checksum)
        capa_transmision(con_ruido)
    
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

# LLAMAR A MAIN
if __name__ == '__main__':
    main()
