import subprocess
import csv
import os
import time
import psutil

from visualizacion import leer_resultados, graficar

# Config
RUTA_EJECUTABLE = "x64/Debug/Bio.exe"
CARPETA_RESULTADOS = "resultados"
RUTA_RESULTADOS = "resultados/resultados_dataset.csv"

K_FIJO = 51

# Genomas
DATASETS = {
    "1mb": ("datos/reads_1mb_1.fq", "datos/reads_1mb_2.fq"),
    "2mb": ("datos/reads_2mb_1.fq", "datos/reads_2mb_2.fq"),
    "3mb": ("datos/reads_3mb_1.fq", "datos/reads_3mb_2.fq"),
    "4.6mb": ("datos/reads_4.6mb_1.fq", "datos/reads_4.6mb_2.fq")
}

def ejecutar_experimentos():
    resultados = []
    os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

    for nombre, (reads1, reads2) in DATASETS.items():
        print(f"\n=== Dataset {nombre} ===")

        fasta = f"datos/reads_{nombre}.fasta"

        # Convertir a FASTA
        subprocess.run([
            "python", "python/fasta.py",
            reads1,
            reads2,
            fasta
        ])

        salida_fasta = f"{CARPETA_RESULTADOS}/contigs_{nombre}.fasta"

        print(f"Ejecutando ensamblador ({nombre}).....")

        start = time.perf_counter()

        process = subprocess.Popen([
            RUTA_EJECUTABLE,
            fasta,
            str(K_FIJO),
            salida_fasta
        ])

        max_mem = 0

        # Va midiendo la memoria, incluye además subprocesos para ser más preciso
        while process.poll() is None:
            try:
                proc = psutil.Process(process.pid)

                mem = proc.memory_info().rss
                for child in proc.children(recursive=True):
                    mem += child.memory_info().rss

                max_mem = max(max_mem, mem)

            except psutil.NoSuchProcess:
                pass

            time.sleep(0.1)

        process.wait()

        # Por si el pico de memoria es al final
        try:
            proc = psutil.Process(process.pid)
            mem = proc.memory_info().rss
            for child in proc.children(recursive=True):
                mem += child.memory_info().rss
            max_mem = max(max_mem, mem)
        except psutil.NoSuchProcess:
            pass

        end = time.perf_counter()
        
        tiempo = end - start
        memoria_mb = max_mem / (1024 ** 2)

        print(f"[Tiempo] {tiempo:.2f} s")
        print(f"[Memoria] {memoria_mb:.2f} MB")

        resultados.append({
            "dataset": nombre,
            "k": K_FIJO,
            "tiempo": tiempo,
            "memoria_mb": memoria_mb
        })

    return resultados


def guardar_csv(resultados):
    with open(RUTA_RESULTADOS, "w", newline="") as f:
        campos = ["dataset", "k", "tiempo", "memoria_mb"]
        writer = csv.DictWriter(f, fieldnames=campos)

        writer.writeheader()
        for fila in resultados:
            writer.writerow(fila)

    print(f"Resultados guardados en {RUTA_RESULTADOS}")


def main():
    resultados = ejecutar_experimentos()
    guardar_csv(resultados)

    tamaños, tiempos, memorias = leer_resultados(RUTA_RESULTADOS)
    graficar(tamaños, tiempos, memorias)


if __name__ == "__main__":
    main()