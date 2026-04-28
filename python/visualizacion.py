import csv
import matplotlib.pyplot as plt
import os

RUTA_CSV = "resultados/resultados.csv"

def leer_resultados(ruta):
    coberturas = []
    n50s = []
    contigs = []
    maximos = []
    totales = []

    with open(ruta, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            coberturas.append(int(fila["cobertura"]))
            n50s.append(int(fila["n50"]))
            contigs.append(int(fila["num_contigs"]))
            maximos.append(int(fila["longitud_maxima"]))
            totales.append(int(fila["longitud_total"]))

    # Ordenar por cobertura
    coberturas, n50s = zip(*sorted(zip(coberturas, n50s)))
    _, contigs = zip(*sorted(zip(coberturas, contigs)))
    _, maximos = zip(*sorted(zip(coberturas, maximos)))
    _, totales = zip(*sorted(zip(coberturas, totales)))

    return coberturas, n50s, contigs, maximos, totales


def graficar(coberturas, n50s, contigs, maximos, totales):
    os.makedirs("resultados", exist_ok=True)

    def plot_metric(valores, ylabel, title, filename):
        plt.figure()
        plt.plot(coberturas, valores, marker='o')

        plt.xlabel("Cobertura (x)")
        plt.ylabel(ylabel)
        plt.title(title)

        plt.xticks(coberturas)
        plt.xlim(min(coberturas) - 2, max(coberturas) + 2)

        plt.ylim(bottom=0)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"resultados/{filename}", dpi=300)
        plt.close()

    # Gráficas de cada métrica
    plot_metric(n50s, "N50", "Cobertura vs N50", "cov_vs_n50.png")
    plot_metric(contigs, "Número de contigs", "Cobertura vs Número de contigs", "cov_vs_contigs.png")
    plot_metric(maximos, "Longitud máxima", "Cobertura vs Longitud máxima", "cov_vs_max.png")
    plot_metric(totales, "Longitud total", "Cobertura vs Longitud total", "cov_vs_total.png")

    # Gráficas todas juntas
    fig, axs = plt.subplots(4, 1, figsize=(8, 16))

    metricas = [
        (n50s, "N50"),
        (contigs, "Número de contigs"),
        (maximos, "Longitud máxima"),
        (totales, "Longitud total")
    ]

    for i, (valores, ylabel) in enumerate(metricas):
        axs[i].plot(coberturas, valores, marker='o')

        axs[i].set_title(f"Cobertura vs {ylabel}")
        axs[i].set_xlabel("Cobertura (x)")
        axs[i].set_ylabel(ylabel)

        axs[i].set_xticks(coberturas)
        axs[i].set_xlim(min(coberturas) - 2, max(coberturas) + 2)

        axs[i].set_ylim(bottom=0)
        axs[i].grid(True)

    plt.tight_layout()
    plt.savefig("resultados/cov_vs_todo.png", dpi=300)
    plt.close()

    print("Gráficas guardadas en carpeta de resultados.")


def main():
    coberturas, n50s, contigs, maximos, totales = leer_resultados(RUTA_CSV)
    graficar(coberturas, n50s, contigs, maximos, totales)


if __name__ == "__main__":
    main()