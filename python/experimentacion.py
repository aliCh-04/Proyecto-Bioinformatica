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

# Con los mejores valores (41, y 31 y 51) 
VALORES_K = [41, 51, 61]
ERRORES = [0, 0.005, 0.01, 0.02]

def ejecutar_experimentos():
    resultados = []
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    for error in ERRORES:
        print(f"\n=== Error {error} ===")

        # Generar reads con ese error
        reads1 = f"datos/reads_e{error}_1.fq"
        reads2 = f"datos/reads_e{error}_2.fq"
        fasta = f"datos/reads_e{error}.fasta"

        # Convertir a fasta
        subprocess.run([
            "python", "python/fasta.py",
            reads1,
            reads2,
            fasta
        ])

        for k in VALORES_K:
            print(f"Ejecutando k={k} con error={error}")

            salida_fasta = f"{CARPETA_RESULTADOS}/contigs_k{k}_e{error}.fasta"

            subprocess.run([
                RUTA_EJECUTABLE,
                fasta,
                str(k),
                salida_fasta
            ])

            longitudes = leer_longitudes_fasta(salida_fasta)
            metricas = calcular_metricas(longitudes)

            metricas["k"] = k
            metricas["error"] = error

            resultados.append(metricas)

    return resultados


def guardar_csv(resultados):
    ruta_csv = f"{CARPETA_RESULTADOS}/resultados.csv"

    with open(ruta_csv, "w", newline="") as f:
        campos = ["k", "error", "num_contigs", "longitud_maxima", "longitud_total", "n50"]
        writer = csv.DictWriter(f, fieldnames=campos)

        writer.writeheader()
        for fila in resultados:
            writer.writerow(fila)

    print(f"Resultados guardados en {ruta_csv}")


def main():
    resultados = ejecutar_experimentos()
    guardar_csv(resultados)

    datos = leer_resultados(RUTA_RESULTADOS)
    graficar(datos)


if __name__ == "__main__":
    main()