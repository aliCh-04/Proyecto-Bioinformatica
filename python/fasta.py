import sys

def fastq_a_fasta(ruta_entrada, ruta_salida):
    with open(ruta_entrada, "r") as f_in, open(ruta_salida, "w") as f_out:
        for i, linea in enumerate(f_in):
            linea = linea.strip()

            if i % 4 == 0:
                header = linea[1:]
                f_out.write(f">{header}\n")

            elif i % 4 == 1:
                f_out.write(f"{linea}\n")


def main():
    if len(sys.argv) < 3:
        print("Uso: python fasta.py <input.fastq> <output.fasta>")
        return

    entrada = sys.argv[1]
    salida = sys.argv[2]

    fastq_a_fasta(entrada, salida)
    print(f"Archivo convertido: {salida}")


if __name__ == "__main__":
    main()