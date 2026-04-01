#include "Kmer.h"
#include <iostream>

using namespace std;

Kmer::Kmer(int valorK) {
	k = valorK;
}

void Kmer::procesarLectura(string_view lectura) {
	if (lectura.length() >= k) {	//Se desecha los que son menores de k
		for (int i = 0; i <= lectura.length() - k; i++) {	//Hasta q no queden bloques k
			string_view kmer = lectura.substr(i, k);	//Se marca el k-mer
			string prefijo = string(kmer.substr(0, k - 1));	//Se coge todo menos la última letro
			char siguiente = kmer.back();	//Se coge el último valor
			diccionario[prefijo].push_back(siguiente);	//Se guarda en el diccionario con clave k -1 letras y valor el de la posición k
		}
	}
}

unordered_map<string, vector<char>>& Kmer::getDiccionario() {
	return diccionario;
}


int Kmer::getK() {
	return k;
}


