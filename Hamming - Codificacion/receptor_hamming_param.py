#!/usr/bin/env python3
import sys


def is_power_two(x):
    return (x & (x - 1)) == 0 and x != 0


def decode(code, n, k):
    if len(code) != n:
        raise ValueError("La longitud de la trama no coincide con n")

    bits = [0] * (n + 1)  # 1-indexado
    # 1. Copiar caracteres de derecha→izquierda para que índice 1 sea el bit LSB
    for idx, ch in enumerate(reversed(code), start=1):
        bits[idx] = int(ch)

    syndrome = 0
    p = 1
    while p <= n:
        parity = 0
        for i in range(1, n + 1):
            if i & p:
                parity ^= bits[i]
        if parity:
            syndrome += p
        p <<= 1

    if syndrome == 0:
        status = "SIN ERRORES"
    elif syndrome <= n:
        status = f"ERROR CORREGIDO en posición {syndrome}"
        bits[syndrome] ^= 1  # corregir
    else:
        return "TRAMA DESCARTADA (error no corregible)"

    # 3. Extraer datos (derecha→izquierda, excluyendo potencias de 2)
    data_bits = [str(bits[i]) for i in range(n, 0, -1) if not is_power_two(i)]
    return f"{status}\nDatos: {''.join(data_bits)}"


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Uso: python3 receptor_hamming_param.py <codigo> <n> <k>", file=sys.stderr
        )
        sys.exit(1)
    trama, n, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    print(decode(trama, n, k))
