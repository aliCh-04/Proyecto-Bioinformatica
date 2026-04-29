import csv
import matplotlib.pyplot as plt
import os

RUTA_CSV = "resultados/resultados.csv"

def leer_resultados(ruta):
    ks = []
    filtros = []
    n50s = []
    num_contigs = []
    max_contigs = []
    long_total = []
    tiempos = []

    with open(ruta, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            ks.append(int(fila["k"]))
            filtros.append(int(fila["filtrar"]))
            n50s.append(int(fila["n50"]))
            num_contigs.append(int(fila["num_contigs"]))
            max_contigs.append(int(fila["longitud_maxima"]))
            long_total.append(int(fila["longitud_total"]))
            tiempos.append(float(fila["tiempo"]))

    return ks, filtros, n50s, num_contigs, max_contigs, long_total, tiempos

def graficar(ks, filtros, n50s, num_contigs, max_contigs, long_total, tiempos):
    os.makedirs("resultados", exist_ok=True)

    def separar_por_filtro(valores):
        con = [v for v, f in zip(valores, filtros) if f == 1]
        sin = [v for v, f in zip(valores, filtros) if f == 0]
        return con, sin

    n50_con, n50_sin = separar_por_filtro(n50s)
    contigs_con, contigs_sin = separar_por_filtro(num_contigs)
    max_con, max_sin = separar_por_filtro(max_contigs)
    total_con, total_sin = separar_por_filtro(long_total)
    tiempo_con, tiempo_sin = separar_por_filtro(tiempos)

    labels = ["sin filtrado", "con filtrado"]

    def plot_bar(valores_sin, valores_con, ylabel, filename):
        plt.figure()
        plt.bar(labels, [valores_sin[0], valores_con[0]])

        plt.ylabel(ylabel)
        plt.title(ylabel)
        plt.grid(axis='y')

        plt.tight_layout()
        plt.savefig(f"resultados/{filename}", dpi=300)
        plt.close()

    plot_bar(n50_sin, n50_con, "N50", "n50.png")
    plot_bar(contigs_sin, contigs_con, "Número de contigs", "contigs.png")
    plot_bar(max_sin, max_con, "Longitud máxima", "max.png")
    plot_bar(total_sin, total_con, "Longitud total", "total.png")
    plot_bar(tiempo_sin, tiempo_con, "Tiempo (s)", "tiempo.png")

    print("Gráficas guardadas en carpeta de resultados.")

def main():
    ks, filtros, n50s, num_contigs, max_contigs, long_total, tiempos = leer_resultados(RUTA_CSV)
    graficar(ks, filtros, n50s, num_contigs, max_contigs, long_total, tiempos)


if __name__ == "__main__":
    main()