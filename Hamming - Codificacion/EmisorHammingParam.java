import java.util.*;

public class EmisorHammingParam {

    private static boolean isPowerOfTwo(int x) {
        return (x & (x - 1)) == 0;
    }

    private static String encodeChunk(String data, int n, int k) {
        int[] code = new int[n + 1]; // 1-indexado
        int j = 0; // índice en data
        for (int i = n; i >= 1; i--) // colocar datos
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

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 1. Leer (n,k) y validar la condición de Hamming
        System.out.print("Ingresa n y k (ej. 7 4): ");
        int n = sc.nextInt(), k = sc.nextInt();
        sc.nextLine();
        int r = n - k, expectedR = 0;
        for (int p = 1; p <= n; p <<= 1)
            expectedR++;
        if (expectedR != r) {
            System.err.println("Par (n,k) no cumple m+r+1 ≤ 2^r.");
            System.exit(1);
        }

        // 2. Leer trama de cualquier longitud
        System.out.print("Mensaje binario (cualquier longitud): ");
        String raw = sc.nextLine().trim();
        if (!raw.matches("[01]+")) {
            System.err.println("Sólo 0/1 permitidos.");
            System.exit(1);
        }

        // 3. Padding para múltiplo de k
        int pad = (k - (raw.length() % k)) % k;
        StringBuilder padded = new StringBuilder(raw);
        for (int i = 0; i < pad; i++)
            padded.append('0');

        // 4. Codificar bloque a bloque
        List<String> words = new ArrayList<>();
        for (int i = 0; i < padded.length(); i += k) {
            String chunk = padded.substring(i, i + k);
            words.add(encodeChunk(chunk, n, k));
        }

        // 5. Mostrar resultados
        System.out.println("\nPadding añadido (ceros): " + pad);
        System.out.println("Palabras Hamming (" + n + "," + k + ") concatenadas:");
        words.forEach(w -> System.out.print(w + ""));
        System.out.println();
        sc.close();
    }
}
