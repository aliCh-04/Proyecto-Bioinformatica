#ifndef KMER_H
#define KMER_H

#include <iostream>
#include <string>
#include <string_view>
#include <unordered_map>
#include <vector>

using namespace std;

class Kmer {
private: 
	int k;
	
	unordered_map<string, vector<char>> grafo;

public:
	Kmer(int valorK);

	void procesarLectura(string_view lectura);

	unordered_map<string, vector<char>>& getGrafo();

	int getK();
};

#endif 
