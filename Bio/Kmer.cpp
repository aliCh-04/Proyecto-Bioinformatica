#include "Kmer.h"

Kmer::Kmer(int valorK) {
	k = valorK;
}

void Kmer::procesarLectura(string_view lectura) {

	if (k <= 1 || lectura.length() < k) {
		cout << "Error: Valor de K no valido o secuencia muy corta." << endl;
		return;
	}

	if (lectura.length() >= k) {	//Se desecha los que son menores de k
		for (int i = 0; i <= lectura.length() - k; i++) {	//Hasta q no queden bloques k
			string_view kmer = lectura.substr(i, k);
			string nodo = string(kmer.substr(0, k - 1));	//Se coge todo menos la �ltima letra
			char arista = kmer.back();	//Se coge el �ltimo valor
			grafo[nodo].push_back(arista);	//Se guarda en el diccionario con clave k -1 letras y valor el de la posici�n k
		}
	}
}

unordered_map<string, vector<char>>& Kmer::getGrafo() {
	return grafo;
}


int Kmer::getK() {
	return k;
}


