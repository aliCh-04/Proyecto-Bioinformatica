import csv
import matplotlib.pyplot as plt
import os

RUTA_CSV = "resultados/resultados.csv"

def leer_resultados(ruta):
    metodos = []
    n50s = []
    num_contigs = []
    max_contigs = []
    long_total = []
    tiempos = []

    with open(ruta, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            metodos.append(fila["metodo"])
            n50s.append(int(fila["n50"]))
            num_contigs.append(int(fila["num_contigs"]))
            max_contigs.append(int(fila["longitud_maxima"]))
            long_total.append(int(fila["longitud_total"]))
            tiempos.append(float(fila["tiempo"]))

    return metodos, n50s, num_contigs, max_contigs, long_total, tiempos


def graficar(metodos, n50s, num_contigs, max_contigs, long_total, tiempos):
    os.makedirs("resultados", exist_ok=True)

    def plot_bar(valores, ylabel, filename):
        plt.figure()
        plt.bar(metodos, valores)

        plt.ylabel(ylabel)
        plt.title(ylabel)
        plt.grid(axis='y')

        plt.tight_layout()
        plt.savefig(f"resultados/{filename}", dpi=300)
        plt.close()

    plot_bar(n50s, "N50", "n50.png")
    plot_bar(num_contigs, "Número de contigs", "contigs.png")
    plot_bar(max_contigs, "Longitud máxima", "max.png")
    plot_bar(long_total, "Longitud total", "total.png")
    plot_bar(tiempos, "Tiempo (s)", "tiempo.png")

    print("Gráficas guardadas en carpeta de resultados.")


def main():
    metodos, n50s, num_contigs, max_contigs, long_total, tiempos = leer_resultados(RUTA_CSV)
    graficar(metodos, n50s, num_contigs, max_contigs, long_total, tiempos)


if __name__ == "__main__":
    main()