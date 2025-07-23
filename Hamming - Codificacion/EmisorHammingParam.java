import java.util.Scanner;

public class EmisorHammingParam {

    private static boolean isPowerOfTwo(int x) {
        return (x & (x - 1)) == 0;
    }

    /**
     * Codifica ‘data’ (k bits) usando Hamming (n,k) con bits de paridad en
     * potencias de 2.
     */
    public static String encode(String data, int n, int k) {
        if (data.length() != k)
            throw new IllegalArgumentException("La trama debe tener k bits exactos.");
        int r = n - k;
        // Verificación básica de la condición de Hamming
        int requiredR = 0;
        for (int p = 1; p <= n; p <<= 1)
            requiredR++;
        if (requiredR != r)
            throw new IllegalArgumentException("n,k no cumplen m+r+1 ≤ 2^r.");

        int[] code = new int[n + 1]; // 1-indexado
        int j = 0; // índice en data

        /* 1. Colocar bits de datos empezando por el índice n hacia 1 (derecha=1). */
        for (int i = n; i >= 1; i--) {
            if (!isPowerOfTwo(i))
                code[i] = data.charAt(j++) - '0';
        }

        /* 2. Calcular bits de paridad (paridad par: V=0, F=1). */
        for (int p = 1; p <= n; p <<= 1) {
            int parity = 0;
            for (int i = 1; i <= n; i++)
                if ((i & p) != 0)
                    parity ^= code[i];
            code[p] = parity; // coloca R1, R2, R4, …
        }

        /* 3. Construir cadena de salida del índice n→1 */
        StringBuilder sb = new StringBuilder();
        for (int i = n; i >= 1; i--)
            sb.append(code[i]);
        return sb.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Ingresa n y k (ej. 11 7): ");
        int n = sc.nextInt(), k = sc.nextInt();
        sc.nextLine();
        System.out.print("Trama binaria (" + k + " bits): ");
        String data = sc.nextLine().trim();

        String encoded = encode(data, n, k);
        System.out.println("Código Hamming (" + n + "," + k + "): " + encoded);
        sc.close();
    }
}
