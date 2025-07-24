#!/usr/bin/env python3
import sys
import textwrap


def is_power_two(x: int) -> bool:
    return (x & (x - 1)) == 0 and x != 0


def decode_chunk(code: str, n: int):
    """Devuelve (estado, datosExtraídos)"""
    bits = [0] + [int(b) for b in reversed(code)]  # 1-indexado

    # 1. Potencias de 2 (excepto n si es global)
    parity_positions = [p for p in range(1, n + 1) if is_power_two(p)]
    has_global = False
    if is_power_two(n):
        has_global = True
        parity_positions.remove(n)  # R8 es global

    # 2. Síndrome
    syndrome = 0
    for p in parity_positions:
        s = 0
        for i in range(1, n + 1):
            if i & p:
                s ^= bits[i]
        if s:
            syndrome |= p

    # 3. Decisión SEC-DED usando R8
    if has_global:
        parity_calc = sum(bits[1:n]) & 1  # XOR de bits 1…(n-1)
        parity_match = parity_calc == bits[n]

        if parity_match and syndrome == 0:  # OK
            status = "SIN ERRORES"

        elif parity_match and syndrome != 0:  # ≥2 errores
            return "DESCARTADO (≥2 errores)", ""

        elif not parity_match and syndrome == 0:  # sólo R8 dañado
            status = f"CORREGIDO bit {n} (paridad global)"
            bits[n] ^= 1

        else:  # 1 solo error en bit S
            status = f"CORREGIDO bit {syndrome}"
            bits[syndrome] ^= 1
    else:
        # Hamming básico (7,4) → sólo SEC
        if syndrome == 0:
            status = "SIN ERRORES"
        elif 1 <= syndrome <= n:
            status = f"CORREGIDO bit {syndrome}"
            bits[syndrome] ^= 1
        else:
            return "DESCARTADO (síndrome inválido)", ""

    # 4. Extraer datos (excluye TODAS las potencias de 2)
    datos = "".join(str(bits[i]) for i in range(n, 0, -1) if not is_power_two(i))
    return status, datos


def main() -> None:
    if len(sys.argv) != 5:
        print(
            "Uso: python receptor_hamming_param.py <codigo> <n> <k> <padding>",
            file=sys.stderr,
        )
        sys.exit(1)

    concat, n, k, pad = (
        sys.argv[1],
        int(sys.argv[2]),
        int(sys.argv[3]),
        int(sys.argv[4]),
    )

    if len(concat) % n != 0:
        print("Longitud del código no múltiplo de n.", file=sys.stderr)
        sys.exit(1)

    bloques = textwrap.wrap(concat, n)
    mensaje = ""
    for idx, cw in enumerate(bloques, 1):
        estado, datos = decode_chunk(cw, n)
        print(f"Bloque {idx}: {estado}  → datos {datos}")
        if estado.startswith("DESCARTADO"):
            continue
        mensaje += datos

    if pad:
        mensaje = mensaje[:-pad]  # quitar ceros de padding
    print("\nMensaje reconstruido:", mensaje)


if __name__ == "__main__":
    main()
