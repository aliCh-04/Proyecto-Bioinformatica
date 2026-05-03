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

    # Ordenar por k
    ks, n50s = zip(*sorted(zip(ks, n50s)))
    ks, num_contigs = zip(*sorted(zip(ks, num_contigs)))
    ks, max_contigs = zip(*sorted(zip(ks, max_contigs)))
    ks, long_total = zip(*sorted(zip(ks, long_total)))

    # Función auxiliar para hacer las gráficas
    def plot_simple(ks, valores, ylabel, title, filename):
        plt.figure()
        plt.plot(ks, valores, marker='o')

        plt.xlabel("k")
        plt.ylabel(ylabel)
        plt.title(title)

        # eje X dinámico
        plt.xlim(min(ks) - 2, max(ks) + 2)
        plt.xticks(ks)

        plt.ylim(bottom=0)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"resultados/{filename}", dpi=300)
        plt.close()

    # Gráficas individuales
    plot_simple(ks, n50s, "N50", "k vs N50", "k_vs_n50.png")
    plot_simple(ks, num_contigs, "Número de contigs", "k vs Número de contigs", "k_vs_contigs.png")
    plot_simple(ks, max_contigs, "Longitud máxima", "k vs Longitud máxima", "k_vs_max.png")
    plot_simple(ks, long_total, "Longitud total", "k vs Longitud total", "k_vs_total.png")

    # Todas las gráficas juntas
    fig, axs = plt.subplots(4, 1, figsize=(8, 16))

    metricas = [
        (n50s, "N50"),
        (num_contigs, "Número de contigs"),
        (max_contigs, "Longitud máxima"),
        (long_total, "Longitud total")
    ]

    for i, (valores, ylabel) in enumerate(metricas):
        axs[i].plot(ks, valores, marker='o')

        axs[i].set_title(f"k vs {ylabel}")
        axs[i].set_xlabel("k")
        axs[i].set_ylabel(ylabel)

        axs[i].set_xlim(min(ks) - 2, max(ks) + 2)
        axs[i].set_xticks(ks)

        axs[i].set_ylim(bottom=0)
        axs[i].grid(True)

    plt.tight_layout()
    plt.savefig("resultados/k_vs_todo.png", dpi=300)
    plt.close()

    print("Gráficas guardadas en carpeta de resultados.")

def main():
    ks, n50s, num_contigs, max_contigs, long_total = leer_resultados(RUTA_CSV)
    graficar(ks, n50s, num_contigs, max_contigs, long_total)


if __name__ == "__main__":
    main()