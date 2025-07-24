import java.util.*;

/**
 * Emisor Hamming (n,k) – admite mensajes de cualquier longitud.
 * Coloca bits de paridad en posiciones potencia de 2 (R1, R2, R4…)
 * y enumera de derecha (bit 1) a izquierda (bit n).
 *
 * Salida:
 * – número de ceros añadidos (padding)
 * – secuencia de palabras Hamming (n bits cada una) separadas por espacio
 */
public class EmisorHammingParam {

    /* ---------- utilidades ---------- */
    private static boolean isPowerOfTwo(int x) {
        return (x & (x - 1)) == 0;
    }

    /** Codifica un bloque de k bits → n bits (derecha→izquierda). */
    private static String encodeChunk(String data, int n, int k) {
        int[] code = new int[n + 1]; // 1-indexado
        int j = 0; // índice en data
        for (int i = n; i >= 1; i--) // colocar bits de datos
            if (!isPowerOfTwo(i))
                code[i] = data.charAt(j++) - '0';

        for (int p = 1; p <= n; p <<= 1) { // bits de paridad
            int parity = 0;
            for (int i = 1; i <= n; i++)
                if ((i & p) != 0)
                    parity ^= code[i];
            code[p] = parity;
        }

        StringBuilder sb = new StringBuilder();
        for (int i = n; i >= 1; i--)
            sb.append(code[i]);
        return sb.toString();
    }

    /* ---------- programa principal ---------- */
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        /* Leer parámetros n y k */
        System.out.print("Ingresa n y k (ej. 7 4): ");
        int n = sc.nextInt(), k = sc.nextInt();
        sc.nextLine();

        /* Verificación mínima m+r+1 ≤ 2^r */
        int requiredR = 0;
        for (int p = 1; p <= n; p <<= 1)
            requiredR++;
        if (requiredR != n - k) {
            System.err.println("Par de valores (n,k) inválido para código de Hamming.");
            System.exit(1);
        }

        /* Leer mensaje */
        System.out.print("Mensaje binario (cualquier longitud): ");
        String raw = sc.nextLine().trim();
        if (!raw.matches("[01]+")) {
            System.err.println("Solo se admiten bits 0 y 1.");
            System.exit(1);
        }

        /* ==== 1. Padding ==== */
        int pad = (k - (raw.length() % k)) % k; // 0-(k-1)
        StringBuilder padded = new StringBuilder(raw);
        for (int i = 0; i < pad; i++)
            padded.append('0');

        /* ==== 2. Codificación bloque a bloque ==== */
        List<String> words = new ArrayList<>();
        for (int i = 0; i < padded.length(); i += k) {
            String chunk = padded.substring(i, i + k);
            words.add(encodeChunk(chunk, n, k));
        }

        /* ==== 3. Salida ==== */
        System.out.println("\nPadding añadido (ceros): " + pad);
        System.out.println("Palabras Hamming (" + n + "," + k + ") concatenadas:");
        words.forEach(w -> System.out.print(w + ""));
        System.out.println();
        sc.close();
    }
}
