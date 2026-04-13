#include <iostream>
#include <fstream>
#include <string>
#include "Kmer.h"

using namespace std;

int main() {
	ifstream datos("secuencias.txt");

	if (!datos.is_open()) {
		cout << "Error: No se ha podido encontrar o abrir el archivo" << endl;
		return 1;
	}

	string linea;
	Kmer aux(4);

	while (getline(datos, linea)) {
		aux.procesarLectura(linea);
	}
	
	datos.close();

	cout << "---ESTADO DEL GRAFO DE BRUIJN---" << endl;
	auto dic = aux.getDiccionario();
	for (auto [nodo, arista] : dic) {
		cout << "[" << nodo << "] ---> ";
		for (char letra : arista) {
			cout << letra << " ";
		}
		cout << endl;
	}
	return 0;
}