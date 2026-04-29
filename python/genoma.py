def genoma(fasta_file):
    total = 0
    secuencia = []

    with open(fasta_file) as f:
        for linea in f:
            if not linea.startswith(">"):
                seq = linea.strip()
                total += len(seq)
                secuencia.append(seq)

    return total, "".join(secuencia)


def cortar_genoma(input_fna, output_fna, tamaño):
    total, secuencia = genoma(input_fna)

    print(f"Tamaño original: {total} bases")

    subseq = secuencia[:tamaño]

    with open(output_fna, "w") as f:
        f.write(">subgenoma\n")
        f.write(subseq)

    print(f"Subgenoma guardado en {output_fna} ({len(subseq)} bases)")
