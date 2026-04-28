import subprocess
import csv
import os

from metricas import leer_longitudes_fasta, calcular_metricas
from visualizacion import leer_resultados, graficar

# Config
RUTA_EJECUTABLE = "x64/Debug/Bio.exe"
CARPETA_RESULTADOS = "resultados"
RUTA_RESULTADOS = "resultados/resultados.csv"

K_FIJO = 51
ERROR_FIJO = 0.01

# Coberturas 
COBERTURAS = [5, 10, 20, 25]

def ejecutar_experimentos():
    resultados = []
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    for cov in COBERTURAS:
        print(f"\n=== Cobertura {cov}x ===")

        # Archivos intermedios
        reads1 = f"datos/reads_cov{cov}_1.fq"
        reads2 = f"datos/reads_cov{cov}_2.fq"
        fasta = f"datos/reads_cov{cov}.fasta"

        # Convertir a FASTA
        subprocess.run([
            "python", "python/fasta.py",
            reads1,
            reads2,
            fasta
        ])

        print(f"Ejecutando ensamblador con k={K_FIJO}, cov={cov}")

        salida_fasta = f"{CARPETA_RESULTADOS}/contigs_k{K_FIJO}_cov{cov}.fasta"

        subprocess.run([
            RUTA_EJECUTABLE,
            fasta,
            str(K_FIJO),
            salida_fasta
        ])

        longitudes = leer_longitudes_fasta(salida_fasta)
        metricas = calcular_metricas(longitudes)

        metricas["k"] = K_FIJO
        metricas["cobertura"] = cov

        resultados.append(metricas)

    return resultados


def guardar_csv(resultados):
    ruta_csv = f"{CARPETA_RESULTADOS}/resultados.csv"

    with open(ruta_csv, "w", newline="") as f:
        campos = ["k", "cobertura", "num_contigs", "longitud_maxima", "longitud_total", "n50"]
        writer = csv.DictWriter(f, fieldnames=campos)

        writer.writeheader()
        for fila in resultados:
            writer.writerow(fila)

    print(f"Resultados guardados en {ruta_csv}")


def main():
    resultados = ejecutar_experimentos()
    guardar_csv(resultados)

    coberturas, n50s, contigs, maximos, totales = leer_resultados(RUTA_RESULTADOS)
    graficar(coberturas, n50s, contigs, maximos, totales)


if __name__ == "__main__":
    main()