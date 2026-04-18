import csv
import matplotlib.pyplot as plt

RUTA_CSV = "resultados/resultados.csv"

def leer_resultados(ruta):
    ks = []
    n50s = []
    num_contigs = []
    max_contigs = []

    with open(ruta, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            ks.append(int(fila["k"]))
            n50s.append(int(fila["n50"]))
            num_contigs.append(int(fila["num_contigs"]))
            max_contigs.append(int(fila["longitud_maxima"]))

    return ks, n50s, num_contigs, max_contigs


def graficar(ks, n50s, num_contigs, max_contigs):
    # k vs N50
    plt.figure()
    plt.plot(ks, n50s, marker='o')
    plt.xlabel("k")
    plt.ylabel("N50")
    plt.title("k vs N50")
    plt.grid(True)
    plt.savefig("resultados/k_vs_n50.png")

    # k vs número de contigs
    plt.figure()
    plt.plot(ks, num_contigs, marker='o')
    plt.xlabel("k")
    plt.ylabel("Número de contigs")
    plt.title("k vs Número de contigs")
    plt.grid(True)
    plt.savefig("resultados/k_vs_contigs.png")

    # k vs longitud máxima de contig
    plt.figure()
    plt.plot(ks, max_contigs, marker='o')
    plt.xlabel("k")
    plt.ylabel("Longitud máxima de contig")
    plt.title("k vs Longitud máxima de contig")
    plt.grid(True)
    plt.savefig("resultados/k_vs_max.png")

    print("Gráficas guardadas en carpeta de resultados.")


def main():
    ks, n50s, num_contigs, max_contigs = leer_resultados(RUTA_CSV)
    graficar(ks, n50s, num_contigs, max_contigs)


if __name__ == "__main__":
    main()