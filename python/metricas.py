import sys

def leer_longitudes_fasta(ruta):
    longitudes = []
    secuencia_actual = ""

    with open(ruta, "r") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue

            if linea.startswith(">"):
                if secuencia_actual:
                    longitudes.append(len(secuencia_actual))
                    secuencia_actual = ""
            else:
                secuencia_actual += linea

        if secuencia_actual:
            longitudes.append(len(secuencia_actual))

    return longitudes


def calcular_n50(longitudes):
    if not longitudes:
        return 0

    longitudes_ordenadas = sorted(longitudes, reverse=True)
    total = sum(longitudes_ordenadas)
    mitad = total // 2

    acumulado = 0
    for l in longitudes_ordenadas:
        acumulado += l
        if acumulado >= mitad:
            return l

    return 0


def calcular_metricas(longitudes):
    if not longitudes:
        return {
            "num_contigs": 0,
            "longitud_maxima": 0,
            "longitud_total": 0,
            "n50": 0
        }

    return {
        "num_contigs": len(longitudes),
        "longitud_maxima": max(longitudes),
        "longitud_total": sum(longitudes),
        "n50": calcular_n50(longitudes)
    }


def main():
    if len(sys.argv) < 2:
        print("Uso: python metricas.py <archivo_fasta>")
        return

    ruta_fasta = sys.argv[1]

    longitudes = leer_longitudes_fasta(ruta_fasta)
    metricas = calcular_metricas(longitudes)

    print("=== MÉTRICAS ===")
    print(f"Numero de contigs: {metricas['num_contigs']}")
    print(f"Longitud maxima: {metricas['longitud_maxima']}")
    print(f"Longitud total: {metricas['longitud_total']}")
    print(f"N50: {metricas['n50']}")


if __name__ == "__main__":
    main()