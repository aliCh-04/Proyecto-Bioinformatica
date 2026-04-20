#include <iostream>
#include <fstream>
#include <string>
#include "Kmer.h"
#include "Ensamblador.h"

using namespace std;

int main(int argc, char* argv[]) {

    if (argc < 4) {
        cout << "Uso: ./assembler <input> <k> <output>" << endl;
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
        // Salto las lineas de encabezado que empiezan con >
        if (linea.empty() || linea[0] == '>') {
            continue;
        }
        // Limpieza, quito espacios y valido caracteres
        for (char& c : linea) {
            c = toupper(c); // Todo a mayusculas
            if (c == 'A' || c == 'C' || c == 'G' || c == 'T') {
                secuencia_completa += c;
            }
        }
        aux.procesarLectura(secuencia_completa);
    }

    datos.close();



    cout << "---ESTADO DEL GRAFO DE BRUIJN---" << endl;
    auto dic = aux.getGrafo();
    for (const auto& [nodo, arista] : dic) {
        cout << "[" << nodo << "] ---> ";
        for (char letra : arista) {
            cout << letra << " ";
        }
        cout << endl;
    }

    cout << "---GENERACION DE CONTIGS---" << endl;
    vector<string> contigs = generador(aux.getGrafo());
    cout << "Se han generado un total de : " << contigs.size() << endl;
    for (int i = 0; i < contigs.size(); i++) {
        cout << "Contig " << i << ": " << contigs[i] << endl;
    }

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