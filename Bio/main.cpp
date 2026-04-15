#include <iostream>
#include <fstream>
#include <string>
#include "Kmer.h"
#include "Ensamblador.h"

using namespace std;

int main() {
	ifstream datos("secuencias.txt");

	if (!datos.is_open()) {
		cout << "Error: No se ha podido encontrar o abrir el archivo" << endl;
		return 1;
	}

	string linea;
	Kmer aux(3);

	while (getline(datos, linea)) {
		aux.procesarLectura(linea);
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

	return 0;
}