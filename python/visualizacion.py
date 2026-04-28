import csv
import matplotlib.pyplot as plt
import os
from collections import defaultdict

RUTA_CSV = "resultados/resultados.csv"

def leer_resultados(ruta):
    datos = defaultdict(lambda: {
        "ks": [],
        "n50": [],
        "contigs": [],
        "max": [],
        "total": []
    })

    with open(ruta, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            error = float(fila["error"])
            datos[error]["ks"].append(int(fila["k"]))
            datos[error]["n50"].append(int(fila["n50"]))
            datos[error]["contigs"].append(int(fila["num_contigs"]))
            datos[error]["max"].append(int(fila["longitud_maxima"]))
            datos[error]["total"].append(int(fila["longitud_total"]))

    return datos


def graficar(datos):
    os.makedirs("resultados", exist_ok=True)

    # Función auxiliar para sacar las gráficas
    def plot_metric(nombre, key, ylabel, filename):
        plt.figure()

        for error, d in datos.items():
            # ordenar por k
            ks = d["ks"]
            valores = d[key]
            ks, valores = zip(*sorted(zip(ks, valores)))

            plt.plot(ks, valores, marker='o', label=f"error={error}")

        plt.xlabel("k")
        plt.ylabel(ylabel)
        plt.title(nombre)
        plt.ylim(bottom=0)
        plt.xlim(left=0)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"resultados/{filename}", dpi=300)
        plt.close()

    # Gráficas individuales
    plot_metric("k vs N50", "n50", "N50", "k_vs_n50.png")
    plot_metric("k vs Número de contigs", "contigs", "Número de contigs", "k_vs_contigs.png")
    plot_metric("k vs Longitud máxima", "max", "Longitud máxima", "k_vs_max.png")
    plot_metric("k vs Longitud total", "total", "Longitud total", "k_vs_total.png")

    # Gráfica con todo
    fig, axs = plt.subplots(4, 1, figsize=(8, 16))

    metricas = [
        ("n50", "N50"),
        ("contigs", "Número de contigs"),
        ("max", "Longitud máxima"),
        ("total", "Longitud total")
    ]

    for i, (key, ylabel) in enumerate(metricas):
        for error, d in datos.items():
            ks = d["ks"]
            valores = d[key]
            ks, valores = zip(*sorted(zip(ks, valores)))

            axs[i].plot(ks, valores, marker='o', label=f"e={error}")

        axs[i].set_title(f"k vs {ylabel}")
        axs[i].set_xlabel("k")
        axs[i].set_ylabel(ylabel)
        axs[i].set_ylim(bottom=0)
        axs[i].set_xlim(left=0)
        axs[i].grid(True)
        axs[i].legend()

    plt.tight_layout()
    plt.savefig("resultados/k_vs_todo.png", dpi=300)
    plt.close()

    print("Gráficas guardadas en carpeta de resultados.")


def main():
    datos = leer_resultados(RUTA_CSV)
    graficar(datos)


if __name__ == "__main__":
    main()