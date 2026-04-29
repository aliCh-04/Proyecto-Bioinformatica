import csv
import matplotlib.pyplot as plt
import os

RUTA_CSV = "resultados/resultados_dataset.csv"

def leer_resultados(ruta):
    filas = []

    with open(ruta, "r") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            # A número
            nombre = fila["dataset"]
            tamaño = float(nombre.replace("mb", ""))

            filas.append((
                tamaño,
                float(fila["tiempo"]),
                float(fila["memoria_mb"])
            ))

    # Ordenar por tamaño
    filas.sort(key=lambda x: x[0])

    tamaños = [f[0] for f in filas]
    tiempos = [f[1] for f in filas]
    memorias = [f[2] for f in filas]

    return tamaños, tiempos, memorias


def graficar(tamaños, tiempos, memorias):
    os.makedirs("resultados", exist_ok=True)

    # Tiempo
    plt.figure()
    plt.plot(tamaños, tiempos, marker='o')
    plt.xlabel("Tamaño del genoma (Mb)")
    plt.ylabel("Tiempo (s)")
    plt.title("Tamaño del dataset vs Tiempo de ejecución")

    plt.xticks(tamaños)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("resultados/dataset_vs_tiempo.png", dpi=300)
    plt.close()

    # Memoria
    plt.figure()
    plt.plot(tamaños, memorias, marker='o')
    plt.xlabel("Tamaño del genoma (Mb)")
    plt.ylabel("Memoria (MB)")
    plt.title("Tamaño del dataset vs Uso de memoria")

    plt.xticks(tamaños)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("resultados/dataset_vs_memoria.png", dpi=300)
    plt.close()

    # Todo junto
    fig, axs = plt.subplots(2, 1, figsize=(8, 10))

    axs[0].plot(tamaños, tiempos, marker='o')
    axs[0].set_title("Tiempo de ejecución")
    axs[0].set_xlabel("Tamaño (Mb)")
    axs[0].set_ylabel("Tiempo (s)")
    axs[0].grid(True)

    axs[1].plot(tamaños, memorias, marker='o')
    axs[1].set_title("Uso de memoria")
    axs[1].set_xlabel("Tamaño (Mb)")
    axs[1].set_ylabel("Memoria (MB)")
    axs[1].grid(True)

    plt.tight_layout()
    plt.savefig("resultados/dataset_vs_todo.png", dpi=300)
    plt.close()

    print("Gráficas de rendimiento guardadas.")


def main():
    tamaños, tiempos, memorias = leer_resultados(RUTA_CSV)
    graficar(tamaños, tiempos, memorias)


if __name__ == "__main__":
    main()