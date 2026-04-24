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



    //cout << "---ESTADO DEL GRAFO DE BRUIJN---" << endl;
    //auto dic = aux.getGrafo();
    //for (const auto& [nodo, arista] : dic) {
    //    cout << "[" << nodo << "] ---> ";
    //    for (char letra : arista) {
    //        cout << letra << " ";
    //    }
    //    cout << endl;
    //}

    cout << "---GENERACION DE CONTIGS---" << endl;
    vector<string> contigs = generador(aux.getGrafo());
    cout << "Se han generado un total de : " << contigs.size() << endl;
    //for (int i = 0; i < contigs.size(); i++) {
    //    cout << "Contig " << i << ": " << contigs[i] << endl;
    //}
    /*
    int cortos = 0;
    int largos = 0;
    for (auto& c : contigs) {
        if (c.size() <= k + 2)cortos++;
        else largos++;
    }
    cout << "Largos: " << largos << endl;
    cout << "Cortos: " << cortos << endl;

    analizarContigs(contigs, k);
    */

    cout << "\n--- METRICAS DEL ENSAMBLAJE ---" << endl;

    int total_contigs = contigs.size();
    long long total_bases = 0;
    int longitud_maxima = 0;

    // Variables para la distribución
    int menores_k = 0;
    int entre_k_y_100 = 0;
    int entre_100_y_500 = 0;
    int mayores_500 = 0;

    for (const string& c : contigs) {
        int len = c.size();
        total_bases += len;

        // Calcular longitud máxima
        if (len > longitud_maxima) {
            longitud_maxima = len;
        }

        // Distribución de longitudes
        if (len <= k + 2) {
            menores_k++; // Contigs muy cortos (ruido o no ensamblados)
        }
        else if (len <= 100) {
            entre_k_y_100++; // Contigs del tamaño de un read
        }
        else if (len <= 500) {
            entre_100_y_500++; // Contigs medianos
        }
        else {
            mayores_500++; // Contigs largos y exitosos
        }
    }

    double longitud_media = total_contigs > 0 ? (double)total_bases / total_contigs : 0.0;

    // Imprimir los resultados exactos que pide el profesor
    cout << "1. Numero total de contigs: " << total_contigs << endl;
    cout << "2. Longitud maxima: " << longitud_maxima << " pb" << endl;
    cout << "3. Longitud media: " << longitud_media << " pb" << endl;
    cout << "4. Distribucion de longitudes:" << endl;
    cout << "   - Muy cortos (<= K+2): " << menores_k << endl;
    cout << "   - Tamano read (hasta 100): " << entre_k_y_100 << endl;
    cout << "   - Medianos (101 - 500): " << entre_100_y_500 << endl;
    cout << "   - Largos (> 500): " << mayores_500 << endl;

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