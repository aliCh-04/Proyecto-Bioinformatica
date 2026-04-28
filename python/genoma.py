def genoma(fasta_file):
    total = 0
    with open(fasta_file) as f:
        for linea in f:
            if not linea.startswith(">"):
                total += len(linea.strip())
    return total

print(genoma("datos/ecoli_completo.fna"))