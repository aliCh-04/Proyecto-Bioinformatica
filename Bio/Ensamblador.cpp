#include "Ensamblador.h"


vector<string> generador(unordered_map<string, vector<char>> grafo) {

	//1. Limpieza del grafo
	unordered_map<string, vector<char>> grafo_limpio;
	for (const auto& [nodo, aristas] : grafo) {
		unordered_map<char, int> frecuencias;

		for (char a : aristas) {
			frecuencias[a]++;
		}

		//Se forma de nuevo el grafo eliminando las aristas q solo han aparecido una vez
		for (char a:aristas) {
			if (frecuencias[a] > 1) {
				grafo_limpio[nodo].push_back(a);
			}
		}
	}

	//2. Calcular la entrada y salida de todos los nodos
	unordered_map<string, int> entradas;
	unordered_map<string, int> salidas;

	for (const auto& [nodo, aristas] : grafo_limpio) {
		unordered_set<char>dest_unicos;
		for (char a : aristas) {
			dest_unicos.insert(a);
		}

		salidas[nodo] += dest_unicos.size();

		for (char a : dest_unicos) {
			string n_destino = nodo.substr(1) + a;
			entradas[n_destino]++;
		}
	}

	//3. Encontrar todos los contigs
	vector<string> contigs;

	for (auto& [nodo, aristas] : grafo_limpio) {
		if (entradas[nodo] == 0 || salidas[nodo] > 1 || entradas[nodo] > 1) { //Hay una bifurcación
			while (!aristas.empty()) {
				string n_actual = nodo;	//El nodo con el que estamos trabajando
				string contig = n_actual;	//El contig que se está formando

				char arista = aristas.back();
				aristas.pop_back();
				contig += arista;
				n_actual = n_actual.substr(1) + arista;

				while (entradas[n_actual] == 1 && salidas[n_actual] == 1) { //Se sigue formando el contig hasta una nueva bifurcación
					if (grafo_limpio[n_actual].empty()) break;

					char siguiente_arista = grafo_limpio[n_actual].back();
					grafo_limpio[n_actual].pop_back();
					contig += siguiente_arista;
					n_actual = n_actual.substr(1) + siguiente_arista;

				}
				contigs.push_back(contig);
			}
		}
	}

	// Para aquellos q no tengan bifurcaciones
	for (auto& [nodo, aristas] : grafo_limpio) {
		if (!aristas.empty()) {
			string n_actual = nodo;
			string contig = n_actual;
			while (!grafo_limpio[n_actual].empty()) {
				char siguiente_arista = grafo_limpio[n_actual].back();
				grafo_limpio[n_actual].pop_back();
				contig += siguiente_arista;
				n_actual = n_actual.substr(1) + siguiente_arista;

			}
			contigs.push_back(contig);
		}
	}
	return contigs;
}