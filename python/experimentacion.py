import subprocess
import csv
import os

from metricas import leer_longitudes_fasta, calcular_metricas
from visualizacion import leer_resultados, graficar

# Config
RUTA_EJECUTABLE = "x64/Debug/Bio.exe"
ARCHIVO_ENTRADA = "datos/reads.fasta"
CARPETA_RESULTADOS = "resultados"
RUTA_RESULTADOS = "resultados/resultados.csv"

VALORES_K = [51, 61]

def ejecutar_experimentos():
    resultados = []

    # Crear carpeta de resultados si no existe
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    for k in VALORES_K:
        print(f"Ejecutando ensamblador con k = {k}")

        salida_fasta = f"{CARPETA_RESULTADOS}/contigs_k{k}.fasta"

        # Ejecutar el ensamblador en c++
        subprocess.run([
            RUTA_EJECUTABLE,
            ARCHIVO_ENTRADA,
            str(k),
            salida_fasta
        ])

        # Calcular métricas
        longitudes = leer_longitudes_fasta(salida_fasta)
        metricas = calcular_metricas(longitudes)

        # Añadir k a resultados
        metricas["k"] = k
        resultados.append(metricas)

    return resultados


def guardar_csv(resultados):
    ruta_csv = f"{CARPETA_RESULTADOS}/resultados.csv"

    with open(ruta_csv, "w", newline="") as f:
        campos = ["k", "num_contigs", "longitud_maxima", "longitud_total", "n50"]
        writer = csv.DictWriter(f, fieldnames=campos)

        writer.writeheader()
        for fila in resultados:
            writer.writerow(fila)

    print(f"Resultados guardados en {ruta_csv}")


def main():
    resultados = ejecutar_experimentos()
    guardar_csv(resultados)

    ks, n50s, num_contigs, max_contigs, long_total = leer_resultados(RUTA_RESULTADOS)
    graficar(ks, n50s, num_contigs, max_contigs, long_total)


if __name__ == "__main__":
    main()