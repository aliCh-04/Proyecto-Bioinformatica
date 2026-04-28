import csv
import matplotlib.pyplot as plt
import os

RUTA_CSV = "resultados/resultados.csv"

def leer_resultados(ruta):
    ks = []
    n50s = []
    num_contigs = []
    max_contigs = []
    long_total = []

    with open(ruta, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            ks.append(int(fila["k"]))
            n50s.append(int(fila["n50"]))
            num_contigs.append(int(fila["num_contigs"]))
            max_contigs.append(int(fila["longitud_maxima"]))
            long_total.append(int(fila["longitud_total"]))

    return ks, n50s, num_contigs, max_contigs, long_total

def graficar(ks, n50s, num_contigs, max_contigs, long_total):
    os.makedirs("resultados", exist_ok=True)

    # Gráficas individuales de cada métrica

    # k vs N50
    plt.figure()
    plt.plot(ks, n50s, marker='o')
    plt.xlabel("k")
    plt.ylabel("N50")
    plt.title("k vs N50")
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("resultados/k_vs_n50.png", dpi=300)
    plt.close()

    # k vs número de contigs
    plt.figure()
    plt.plot(ks, num_contigs, marker='o')
    plt.xlabel("k")
    plt.ylabel("Número de contigs")
    plt.title("k vs Número de contigs")
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("resultados/k_vs_contigs.png", dpi=300)
    plt.close()

    # k vs longitud máxima de contig
    plt.figure()
    plt.plot(ks, max_contigs, marker='o')
    plt.xlabel("k")
    plt.ylabel("Longitud máxima de contig")
    plt.title("k vs Longitud máxima de contig")
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("resultados/k_vs_max.png", dpi=300)
    plt.close()

    # k vs longitud total
    plt.figure()
    plt.plot(ks, long_total, marker='o')
    plt.xlabel("k")
    plt.ylabel("Longitud total ensamblada")
    plt.title("k vs Longitud total")
    plt.ylim(bottom=0)
    plt.xlim(left=0)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("resultados/k_vs_total.png", dpi=300)
    plt.close()

    # Figura con todas las gráficas juntas

    fig, axs = plt.subplots(4, 1, figsize=(8, 16))

    # N50
    axs[0].plot(ks, n50s, marker='o')
    axs[0].set_title("k vs N50")
    axs[0].set_xlabel("k")
    axs[0].set_ylabel("N50")
    axs[0].set_ylim(bottom=0)
    axs[0].set_xlim(left=0)
    axs[0].grid(True)

    # Contigs
    axs[1].plot(ks, num_contigs, marker='o')
    axs[1].set_title("k vs Número de contigs")
    axs[1].set_xlabel("k")
    axs[1].set_ylabel("Número de contigs")
    axs[1].set_ylim(bottom=0)
    axs[1].set_xlim(left=0)
    axs[1].grid(True)

    # Max contig
    axs[2].plot(ks, max_contigs, marker='o')
    axs[2].set_title("k vs Longitud máxima de contig")
    axs[2].set_xlabel("k")
    axs[2].set_ylabel("Longitud máxima")
    axs[2].set_ylim(bottom=0)
    axs[2].set_xlim(left=0)
    axs[2].grid(True)

    # Longitud total
    axs[3].plot(ks, long_total, marker='o')
    axs[3].set_title("k vs Longitud total ensamblada")
    axs[3].set_xlabel("k")
    axs[3].set_ylabel("Longitud total")
    axs[3].set_ylim(bottom=0)
    axs[3].set_xlim(left=0)
    axs[3].grid(True)

    plt.tight_layout()
    plt.savefig("resultados/k_vs_todo.png", dpi=300)
    plt.close()

    print("Gráficas guardadas en carpeta de resultados.")

def main():
    ks, n50s, num_contigs, max_contigs, long_total = leer_resultados(RUTA_CSV)
    graficar(ks, n50s, num_contigs, max_contigs, long_total)


if __name__ == "__main__":
    main()