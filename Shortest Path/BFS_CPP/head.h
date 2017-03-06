#include <iostream>
#include <vector>
#include <string> 
#include <fstream>  

using namespace std;

#define NODES_TOTAL 14951
typedef unsigned char byte;

extern byte graph[NODES_TOTAL][NODES_TOTAL];


int build_bi_graph();
string BFS(int source,int target,int max_length=5);
vector<string> split(string& str,const char* c);