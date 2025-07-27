import java.util.*;
import java.net.*;
import java.io.*;

public class CombinedEmisor {

    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);

        // ─── Capa de Aplicación ────────────────────────────────
        System.out.print("Seleccione algoritmo (fletcher/hamming): ");
        String algo = sc.nextLine().trim().toLowerCase();

        System.out.print("Mensaje a enviar: ");
        String message = sc.nextLine();

        int blockSize = 0, n = 0, k = 0;
        if (algo.equals("fletcher")) {
            System.out.print("Tamaño de bloque Fletcher (8/16/32): ");
            blockSize = sc.nextInt();
        } else if (algo.equals("hamming")) {
            System.out.print("n (longitud total del código): ");
            n = sc.nextInt();
            System.out.print("k (bits de datos por bloque): ");
            k = sc.nextInt();
        } else {
            System.err.println("Algoritmo no soportado.");
            sc.close();
            return;
        }

        // ─── Capa de Ruido (entrada de probabilidad) ────────────
        System.out.print("Tasa de error (p.ej. 0.01 para 1%): ");
        double errorRate = sc.nextDouble();
        sc.nextLine();  // limpiar buffer

        System.out.print("Host receptor: ");
        String host = sc.nextLine();

        System.out.print("Puerto receptor: ");
        int port = sc.nextInt();
        sc.nextLine();  // limpiar buffer

        // ─── Capa de Presentación ───────────────────────────────
        StringBuilder dataBits = new StringBuilder();
        for (char c : message.toCharArray()) {
            dataBits.append(
                String.format("%8s", Integer.toBinaryString(c))
                      .replace(' ', '0')
            );
        }

        // ─── Capa de Enlace ─────────────────────────────────────
        String frame;
        if (algo.equals("fletcher")) {
            long[] chk = computeFletcher(dataBits.toString(), blockSize);
            String chk1 = padLeft(Long.toBinaryString(chk[0]), blockSize);
            String chk2 = padLeft(Long.toBinaryString(chk[1]), blockSize);
            frame = dataBits.toString() + chk1 + chk2;

        } else {
            // Hamming
            int pad = (k - (dataBits.length() % k)) % k;
            for (int i = 0; i < pad; i++) dataBits.append('0');
            System.out.println("Bits de padding añadidos: " + pad);

            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < dataBits.length(); i += k) {
                sb.append(encodeHamming(dataBits.substring(i, i + k), n));
            }
            frame = sb.toString();

            // ─── Inyección automática de 1 bit de error en bloque 1 ───
            System.out.print("¿Inyectar prueba de error de 1 bit en bloque 1? (s/n): ");
            String inj = sc.nextLine().trim().toLowerCase();
            if (inj.equals("s")) {
                StringBuilder tmp = new StringBuilder(frame);
                int flipIdx = 2;  // tercer bit del primer bloque (0-based)
                char orig = tmp.charAt(flipIdx);
                tmp.setCharAt(flipIdx, orig=='0'?'1':'0');
                frame = tmp.toString();
                System.out.println("Error de prueba aplicado: flip en bit 3 del bloque 1");
            }
        }

        // ─── Capa de Ruido ──────────────────────────────────────
        String noisy = applyNoise(frame, errorRate);

        // ─── Capa de Transmisión ────────────────────────────────
        try (Socket socket = new Socket(host, port);
             PrintWriter out = new PrintWriter(socket.getOutputStream(), true)) {
            out.print(noisy);
        }
        System.out.println("Trama enviada: " + noisy);
        sc.close();
    }

    // ─── Métodos auxiliares ────────────────────────────────
    static long[] computeFletcher(String data, int B) {
        long mod = (1L << B) - 1, sum1 = 0, sum2 = 0;
        for (int i = 0; i < data.length(); i += B) {
            int end = Math.min(i + B, data.length());
            int word = Integer.parseInt(data.substring(i, end), 2);
            sum1 = (sum1 + word) % mod;
            sum2 = (sum2 + sum1) % mod;
        }
        return new long[]{sum1, sum2};
    }

    static String encodeHamming(String data, int n) {
        List<Integer> ppos = new ArrayList<>();
        for (int p = 1; p < n; p <<= 1) ppos.add(p);
        boolean hasGlobal = (n & (n - 1)) == 0;
        int[] bits = new int[n+1];
        int di = 0;
        for (int i = 1; i <= n; i++) {
            if (!ppos.contains(i) && !(hasGlobal && i==n)) {
                bits[i] = data.charAt(di++) - '0';
            }
        }
        for (int p: ppos) {
            int s = 0;
            for (int i = 1; i <= n; i++) if ((i&p)!=0) s ^= bits[i];
            bits[p] = s;
        }
        if (hasGlobal) {
            int s=0; for(int i=1;i<n;i++) s^=bits[i];
            bits[n]=s;
        }
        StringBuilder cw = new StringBuilder();
        for (int i = n; i >= 1; i--) cw.append(bits[i]);
        return cw.toString();
    }

    static String applyNoise(String frame, double p) {
        Random rnd = new Random();
        StringBuilder sb = new StringBuilder(frame.length());
        for (char b: frame.toCharArray()) {
            sb.append(rnd.nextDouble() < p ? (b=='0'?'1':'0') : b);
        }
        return sb.toString();
    }

    static String padLeft(String s, int width) {
        return String.format("%" + width + "s", s).replace(' ', '0');
    }
}
