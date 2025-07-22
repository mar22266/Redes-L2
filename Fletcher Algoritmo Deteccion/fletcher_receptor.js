// Andre Marroquin 

// lee la entrada de usuario
const readline = require('readline');

// funcion que calcula el checksum de Fletcher
function computeFletcher(dataBits, blockSize) {
  const mod = Math.pow(2, blockSize) - 1;
  let sum1 = 0, sum2 = 0;
  for (let i = 0; i < dataBits.length; i += blockSize) {
    const word = parseInt(dataBits.slice(i, i + blockSize), 2);
    sum1 = (sum1 + word) % mod;
    sum2 = (sum2 + sum1) % mod;
  }
  return { sum1, sum2 };
}

// funcion que verifica el checksum de Fletcher
function verifyFletcher(frame, blockSize) {
  const totalBits = frame.length;
  const chkBits = 2 * blockSize;
  if (totalBits <= chkBits) {
    console.error("Trama demasiado corta para contener checksum.");
    process.exit(1);
  }

  // Separar los bits de datos y los checksums
  const dataBits = frame.slice(0, totalBits - chkBits);
  const chk1_bits = frame.slice(totalBits - chkBits, totalBits - blockSize);
  const chk2_bits = frame.slice(totalBits - blockSize);

  const received1 = parseInt(chk1_bits, 2);
  const received2 = parseInt(chk2_bits, 2);
  const { sum1, sum2 } = computeFletcher(dataBits, blockSize);

  // Verificar si los checksums coinciden
  if (sum1 === received1 && sum2 === received2) {
    console.log("Trama válida. No se detectaron errores.");
    console.log("Datos originales:", dataBits);
  } else {
    console.log("Error detectado en la trama.");
    console.log(`Checksum recibido: (${received1}, ${received2})`);
    console.log(`Checksum calculado: (${sum1}, ${sum2})`);
  }
}

// Interfaz de línea de comandos para recibir entrada del usuario
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});
rl.question("Ingrese la trama (datos+checksum) en binario: ", frame => {
  rl.question("Tamaño de bloque usado (8, 16 o 32): ", bs => {
    const block = parseInt(bs.trim(), 10);
    if (![8,16,32].includes(block)) {
      console.error("block size inválido.");
      process.exit(1);
    }
    verifyFletcher(frame.trim(), block);
    rl.close();
  });
});
