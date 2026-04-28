import csv
import matplotlib.pyplot as plt
import os

RUTA_CSV = "resultados/resultados.csv"

def leer_resultados(ruta):
    filas = []

    with open(ruta, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            filas.append((
                int(fila["cobertura"]),
                int(fila["n50"]),
                int(fila["num_contigs"]),
                int(fila["longitud_maxima"]),
                int(fila["longitud_total"])
            ))

    # Ordenar por cobertura
    filas.sort(key=lambda x: x[0])

    coberturas = [f[0] for f in filas]
    n50s = [f[1] for f in filas]
    contigs = [f[2] for f in filas]
    maximos = [f[3] for f in filas]
    totales = [f[4] for f in filas]

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