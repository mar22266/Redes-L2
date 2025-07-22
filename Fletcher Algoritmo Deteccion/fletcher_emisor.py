# Andre Marroquin
# importar librerias
import sys

# funcion para calcular el checksum de Fletcher
def fletcher_checksum(data_bits: str, block_size: int) -> str:
    # Validar block_size
    if block_size not in (8, 16, 32):
        raise ValueError("block_size debe ser 8, 16 o 32")
    # ajustar block_size a bits
    length = len(data_bits)
    if length < block_size or (length % block_size != 0):
        pad_len = ((length + block_size - 1) // block_size) * block_size - length
        data_bits += '0' * pad_len

    # Partir en bloques y convertir a enteros
    mod = (1 << block_size) - 1
    sum1 = 0
    sum2 = 0
    for i in range(0, len(data_bits), block_size):
        word = int(data_bits[i:i+block_size], 2)
        sum1 = (sum1 + word) % mod
        sum2 = (sum2 + sum1) % mod

    # Formatear checksum como dos palabras de block_size bits
    chk1 = format(sum1, f'0{block_size}b')
    chk2 = format(sum2, f'0{block_size}b')

    # devolver trama + checksum
    return data_bits + chk1 + chk2

# funcion principal para interactuar con el usuario
def main():
    raw = input("Ingrese la trama en binario: ").strip()
    try:
        block = int(input("Tamaño de bloque (8, 16 o 32): ").strip())
        framed = fletcher_checksum(raw, block)
        print("\n> Trama enviada (datos + checksum):")
        print(framed)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

# llamar a la funcion principal
if __name__ == '__main__':
    main()
