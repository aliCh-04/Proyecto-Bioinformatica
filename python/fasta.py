import sys

# Convierte de fastq a fasta
def fastq_a_fasta(rutas_entrada, ruta_salida):
    with open(ruta_salida, "w") as f_out:
        for ruta in rutas_entrada:
            with open(ruta, "r") as f_in:
                for i, linea in enumerate(f_in):
                    linea = linea.strip()

                    if i % 4 == 0:
                        header = linea[1:]
                        f_out.write(f">{header}\n")

                    elif i % 4 == 1:
                        f_out.write(f"{linea}\n")


def main():
    if len(sys.argv) < 3:
        print("Uso: python fasta.py <input1.fastq> <input2.fastq> <output.fasta>")
        return

    *entradas, salida = sys.argv[1:]
    fastq_a_fasta(entradas, salida)
    print(f"Archivo convertido: {salida}")


if __name__ == "__main__":
    main()