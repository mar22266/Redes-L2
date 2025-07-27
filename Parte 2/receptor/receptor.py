import socket
import textwrap

def compute_fletcher(data, B):
    mod = (1 << B) - 1
    s1 = s2 = 0
    for i in range(0, len(data), B):
        word = int(data[i:i+B], 2)
        s1 = (s1 + word) % mod
        s2 = (s2 + s1) % mod
    return s1, s2

def verify_fletcher(frame, B):
    total = len(frame)
    chk_bits = 2 * B
    data_bits = frame[:total - chk_bits]
    r1 = int(frame[total - chk_bits : total - B], 2)
    r2 = int(frame[total - B :], 2)
    s1, s2 = compute_fletcher(data_bits, B)
    return (s1 == r1 and s2 == r2), data_bits, (r1, r2), (s1, s2)

def is_power_two(x):
    return (x & (x-1)) == 0 and x != 0

def decode_hamming_chunk(code, n):
    # Reconstruir array 1‑indexado igual que en emisor
    bits = [0] + [int(b) for b in reversed(code)]
    # posiciones de paridad
    ppos = [p for p in range(1, n) if is_power_two(p)]
    has_global = is_power_two(n)

    # Cálculo de síndrome
    syndrome = 0
    for p in ppos:
        s = 0
        for i in range(1, n+1):
            if i & p:
                s ^= bits[i]
        if s:
            syndrome |= p

    # Corrección según síndrome y paridad global si existe
    if has_global:
        global_ok = ((sum(bits[1:n]) & 1) == bits[n])
        if global_ok and syndrome == 0:
            status = "SIN ERRORES"
        elif global_ok and syndrome != 0:
            return "DESCARTADO (≥2 errores)", ""
        elif not global_ok and syndrome == 0:
            status = f"CORREGIDO bit {n} (paridad global)"
            bits[n] ^= 1
        else:
            status = f"CORREGIDO bit {syndrome}"
            bits[syndrome] ^= 1
    else:
        if syndrome == 0:
            status = "SIN ERRORES"
        elif 1 <= syndrome <= n:
            status = f"CORREGIDO bit {syndrome}"
            bits[syndrome] ^= 1
        else:
            return "DESCARTADO", ""

    dpos = [i for i in range(1, n+1) if not is_power_two(i)]
    data_bits = "".join(str(bits[i]) for i in dpos)
    return status, data_bits

def main():
    # Capa de Aplicación
    algo = input("Seleccione algoritmo (fletcher/hamming): ").strip().lower()
    if algo == "fletcher":
        B = int(input("Tamaño de bloque Fletcher (8/16/32): "))
    elif algo == "hamming":
        n = int(input("n (longitud total del código): "))
        k = int(input("k (bits de datos por bloque): "))
        pad = int(input("Padding aplicado en emisor: "))
    else:
        print("Algoritmo no soportado.")
        return

    port = int(input("Puerto a escuchar: "))

    # Capa de Transmisión
    srv = socket.socket()
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("", port))
    srv.listen(1)
    print(f"Receptor escuchando en puerto {port}…")

    try:
        while True:
            conn, _ = srv.accept()
            with conn:
                frame = conn.recv(65536).decode().strip()
            print("\nTrama recibida:", frame)

            # Capa de Enlace
            if algo == "fletcher":
                ok, data_bits, (r1, r2), (s1, s2) = verify_fletcher(frame, B)
                if not ok:
                    print(f"ERROR checksum inválido: recibido=({r1},{r2}) calculado=({s1},{s2})")
                    continue
                print("Checksum válido. No se detectaron errores.")
            else:
                bloques = textwrap.wrap(frame, n)
                data_bits = ""
                for i, cw in enumerate(bloques, 1):
                    status, db = decode_hamming_chunk(cw, n)
                    print(f"Bloque {i}: {status} → datos {db}")
                    if not status.startswith("DESCARTADO"):
                        data_bits += db
                if pad:
                    data_bits = data_bits[:-pad]

            #Capa de Presentación
            message = "".join(
                chr(int(data_bits[i:i+8], 2))
                for i in range(0, len(data_bits), 8)
            )

            # Capa de Aplicación 
            print("Mensaje recibido:", message)

    except KeyboardInterrupt:
        print("\nReceptor interrumpido, cerrando.")
    finally:
        srv.close()

if __name__ == "__main__":
    main()
