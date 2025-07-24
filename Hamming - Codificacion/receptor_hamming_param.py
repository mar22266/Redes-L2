#!/usr/bin/env python3
"""
Receptor Hamming (n,k) – admite secuencia de palabras concatenadas.
Corrige 1 error por palabra, detecta ≥2 errores (bloque descartado).
El último argumento CLI indica cuántos ceros de padding añadió el emisor.
"""

import sys
import textwrap


def is_power_two(x: int) -> bool:
    return (x & (x - 1)) == 0 and x != 0


def decode_chunk(code: str, n: int):
    bits = [0] + [int(b) for b in reversed(code)]  # 1-indexado
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
    elif 1 <= syndrome <= n:
        status = f"CORREGIDO bit {syndrome}"
        bits[syndrome] ^= 1
    else:
        return "DESCARTADO", ""

    datos = "".join(str(bits[i]) for i in range(n, 0, -1) if not is_power_two(i))
    return status, datos


def main() -> None:
    if len(sys.argv) != 5:
        print(
            "Uso: python3 receptor_hamming_param.py <codigo> <n> <k> <padding>",
            file=sys.stderr,
        )
        sys.exit(1)

    concat = sys.argv[1]
    n = int(sys.argv[2])
    k = int(sys.argv[3])
    pad = int(sys.argv[4])

    if len(concat) % n != 0:
        print("Longitud del código no es múltiplo de n.", file=sys.stderr)
        sys.exit(1)

    bloques = textwrap.wrap(concat, n)
    mensaje = ""
    for idx, cw in enumerate(bloques, 1):
        st, datos = decode_chunk(cw, n)
        print(f"Bloque {idx}: {st}  → datos {datos}")
        if st != "DESCARTADO":
            mensaje += datos

    if pad:
        mensaje = mensaje[:-pad]  # quitar ceros añadidos por el emisor

    print("\nMensaje reconstruido:", mensaje)


if __name__ == "__main__":
    main()
