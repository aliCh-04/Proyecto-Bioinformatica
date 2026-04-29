#include "Ensamblador.h"

vector<string> generador(unordered_map<string, vector<char>> grafo, bool filtrar) {

    unordered_map<string, vector<char>> grafo_trabajo;

    if (filtrar) {
        //1. Limpieza del grafo
        for (const auto& [nodo, aristas] : grafo) {
            unordered_map<char, int> frecuencias;

            for (char a : aristas) {
                frecuencias[a]++;
            }

            for (char a : aristas) {
                if (frecuencias[a] > 1) {
                    grafo_trabajo[nodo].push_back(a);
                }
            }
        }
    } else {
        grafo_trabajo = grafo;
    }

    //2. Calcular la entrada y salida de todos los nodos
    unordered_map<string, int> entradas;
    unordered_map<string, int> salidas;

    for (const auto& [nodo, aristas] : grafo_trabajo) {
        unordered_set<char> dest_unicos;
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

    for (auto& [nodo, aristas] : grafo_trabajo) {
        if (entradas[nodo] == 0 || salidas[nodo] > 1 || entradas[nodo] > 1) {
            while (!aristas.empty()) {
                string n_actual = nodo;
                string contig = n_actual;

                char arista = aristas.back();
                aristas.pop_back();
                contig += arista;
                n_actual = n_actual.substr(1) + arista;

                while (entradas[n_actual] == 1 && salidas[n_actual] == 1) {
                    if (grafo_trabajo[n_actual].empty()) break;

                    char siguiente_arista = grafo_trabajo[n_actual].back();
                    grafo_trabajo[n_actual].pop_back();
                    contig += siguiente_arista;
                    n_actual = n_actual.substr(1) + siguiente_arista;
                }
                contigs.push_back(contig);
            }
        }
    }

    // Para aquellos sin bifurcaciones
    for (auto& [nodo, aristas] : grafo_trabajo) {
        if (!aristas.empty()) {
            string n_actual = nodo;
            string contig = n_actual;
            while (!grafo_trabajo[n_actual].empty()) {
                char siguiente_arista = grafo_trabajo[n_actual].back();
                grafo_trabajo[n_actual].pop_back();
                contig += siguiente_arista;
                n_actual = n_actual.substr(1) + siguiente_arista;
            }
            contigs.push_back(contig);
        }
    }

    return contigs;
}