import subprocess
import csv
import os
import time
from metricas import leer_longitudes_fasta, calcular_metricas
from visualizacion import leer_resultados, graficar

# Config
RUTA_EJECUTABLE = "x64/Debug/Bio.exe"
ARCHIVO_ENTRADA = "datos/reads.fasta"
CARPETA_RESULTADOS = "resultados"
RUTA_RESULTADOS = "resultados/resultados.csv"

K_FIJO = 51

def ejecutar_experimentos():
    resultados = []

    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    for filtrar in [0, 1]:
        print(f"Ejecutando ensamblador k={K_FIJO}, filtrar={filtrar}")

        salida_fasta = f"{CARPETA_RESULTADOS}/contigs_k{K_FIJO}_f{filtrar}.fasta"

        start = time.perf_counter()

        subprocess.run([
            RUTA_EJECUTABLE,
            ARCHIVO_ENTRADA,
            str(K_FIJO),
            salida_fasta,
            str(filtrar)
        ])

        end = time.perf_counter()

        tiempo = end - start

        longitudes = leer_longitudes_fasta(salida_fasta)
        metricas = calcular_metricas(longitudes)

        metricas["k"] = K_FIJO
        metricas["filtrar"] = filtrar
        metricas["tiempo"] = tiempo  

        resultados.append(metricas)

    return resultados

def guardar_csv(resultados):
    ruta_csv = f"{CARPETA_RESULTADOS}/resultados.csv"

    with open(ruta_csv, "w", newline="") as f:
        campos = ["k", "filtrar", "num_contigs", "longitud_maxima", "longitud_total", "n50", "tiempo"]
        writer = csv.DictWriter(f, fieldnames=campos)

        writer.writeheader()
        for fila in resultados:
            writer.writerow(fila)

    print(f"Resultados guardados en {ruta_csv}")


def main():
    resultados = ejecutar_experimentos()
    guardar_csv(resultados)

    ks, filtros, n50s, num_contigs, max_contigs, long_total, tiempos = leer_resultados(RUTA_RESULTADOS)
    graficar(ks, filtros, n50s, num_contigs, max_contigs, long_total, tiempos)


if __name__ == "__main__":
    main()