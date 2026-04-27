#include <iostream>
#include <fstream>
#include <string>
#include "Kmer.h"
#include "Ensamblador.h"

using namespace std;


void analizarContigs(const vector<string>& contigs, int k) {
    long long total_bases = 0;
    long long bases_k_approx = 0;
    long long bases_100_approx = 0;
    long long bases_gt_100 = 0;
    long long bases_gt_500 = 0;

    int count_k_approx = 0;
    int count_100_approx = 0;
    int count_gt_100 = 0;
    int count_gt_500 = 0;

    for (const auto& c : contigs) {
        int len = c.size();
        total_bases += len;

        if (len >= k && len <= k + 5) {
            bases_k_approx += len;
            count_k_approx++;
        }

        if (len >= 95 && len <= 105) {
            bases_100_approx += len;
            count_100_approx++;
        }

        if (len > 100) {
            bases_gt_100 += len;
            count_gt_100++;
        }

        if (len > 500) {
            bases_gt_500 += len;
            count_gt_500++;
        }
    }

    cout << "\n===== ANALISIS DE CONTIGS =====" << endl;
    cout << "Total bases: " << total_bases << endl;

    cout << "\n--- ~k ---" << endl;
    cout << "Contigs: " << count_k_approx << endl;
    cout << "Bases: " << bases_k_approx << endl;
    cout << "%: " << (double)bases_k_approx / total_bases << endl;

    cout << "\n--- ~100 ---" << endl;
    cout << "Contigs: " << count_100_approx << endl;
    cout << "Bases: " << bases_100_approx << endl;
    cout << "%: " << (double)bases_100_approx / total_bases << endl;

    cout << "\n--- >100 ---" << endl;
    cout << "Contigs: " << count_gt_100 << endl;
    cout << "Bases: " << bases_gt_100 << endl;
    cout << "%: " << (double)bases_gt_100 / total_bases << endl;

    cout << "\n--- >500 ---" << endl;
    cout << "Contigs: " << count_gt_500 << endl;
    cout << "Bases: " << bases_gt_500 << endl;
    cout << "%: " << (double)bases_gt_500 / total_bases << endl;
}

int main(int argc, char* argv[]) {

    if (argc < 4) {
        cout << "Uso: ./main <input> <k> <output>" << endl;
        cout << "En el Visual Studio, ir a Proyecto -> Propiedades -> Depuración -> Argumentos de comando, y ponerlo ahi." << endl;
        return 1;
    }

    string inputFile = argv[1];
    int k = stoi(argv[2]);
    string outputFile = argv[3];

    ifstream datos(inputFile);

    if (!datos.is_open()) {
        cout << "Error: No se ha podido encontrar o abrir el archivo" << endl;
        return 1;
    }

    string linea;
    Kmer aux(k);
    string secuencia_completa;

    while (getline(datos, linea)) {
        if (linea.empty() || linea[0] == '>') {
            continue;
        }

        string secuencia_limpia;

        for (char c : linea) {
            c = toupper(c);
            if (c == 'A' || c == 'C' || c == 'G' || c == 'T') {
                secuencia_limpia += c;
            }
        }

        aux.procesarLectura(secuencia_limpia);
    }

    datos.close();

    cout << "---GENERACION DE CONTIGS---" << endl;
    vector<string> contigs = generador(aux.getGrafo());
    cout << "Se han generado un total de : " << contigs.size() << endl;

    int cortos = 0;
    int largos = 0;
    for (auto& c : contigs) {
        if (c.size() <= k + 2)cortos++;
        else largos++;
    }
    cout << "Largos: " << largos << endl;
    cout << "Cortos: " << cortos << endl;

    analizarContigs(contigs, k);

    // Guardar contigs en formato FASTA
    ofstream out(outputFile);

    if (!out.is_open()) {
        cout << "Error: No se ha podido crear el archivo de salida" << endl;
        return 1;
    }

    for (int i = 0; i < contigs.size(); i++) {
        out << ">contig_" << i << "\n";
        out << contigs[i] << "\n";
    }

    out.close();

    return 0;
}