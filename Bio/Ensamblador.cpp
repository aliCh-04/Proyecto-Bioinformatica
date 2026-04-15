#include "Ensamblador.h"


string ensamblador(unordered_map<string, vector<char>> grafo) {

	//1. Búsqueda del nodo inicial y el nodo final
	unordered_map<string, int> entradas;
	unordered_map<string, int> salidas;

	for (const auto& [nodo, aristas] : grafo) {
		salidas[nodo] += aristas.size();
		for (char a : aristas) {
			string n_destino = nodo.substr(1) + a;
			entradas[n_destino]++;
		}
	}

	string nodo_inicial = grafo.begin()->first;
	for (const auto& [nodo, cantidad] : salidas) {
		if (cantidad - entradas[nodo] == 1) { //Si un nodo tiene una arista de salida más q una de entrada entonces es un NODO INICIAL
			nodo_inicial = nodo;
			break;
		}
	}

	//2. Camino euleriano
	stack<string>pila;
	deque<string>camino;

	pila.push(nodo_inicial);

	while (!pila.empty()) {
		string n_actual = pila.top();
		if (!grafo[n_actual].empty()) { //Existen otros caminos
			char arista = grafo[n_actual].back();
			grafo[n_actual].pop_back();

			string n_destino = n_actual.substr(1) + arista;
			pila.push(n_destino);
		}
		else {
			camino.push_front(n_actual);
			pila.pop();
		}
	}

	//3. Construcción del resultado final
	string resultado = camino.front();
	camino.pop_front();
	while (!camino.empty()) {
		resultado += camino.front().back();
		camino.pop_front();
	}
	return resultado;
}