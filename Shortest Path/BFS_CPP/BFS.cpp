#include <head.h>
#include <vector>
#include <stack>

//extern byte graph[NODES_TOTAL][NODES_TOTAL];


string BFS(int source,int target,int max_length)
{
	vector<int> order;
	order.push_back(source);
	int crawled_node[NODES_TOTAL];

	for(int i=0;i<NODES_TOTAL;i++)
		crawled_node[i] = -1;


	crawled_node[source] = true;

	// É¾³ýÏÖÓÐ±ß
	int delete_edge = graph[source][target] & 0x1;
	graph[source][target] &= 0x0;

	int length = 1;
	bool isFindPath = false;
	while (length < max_length)
	{
		vector<int> next;

		for(int node:order)
		{
			for(int i=0;i<NODES_TOTAL;i++)
			{
				if(graph[node][i] & 0x1 == 1 && crawled_node[i]==-1)
				{
					next.push_back(i);
					crawled_node[i]=node;

					if(i==target)
					{
						isFindPath = true;
						goto find_path;
					}
				}
			}
		}
		order = next;

		length += 1;
	}

	

find_path:
	string path="";
	if(isFindPath)
	{
		stack<int> path_stack;
		
		int node = target;
		
		while(node != source)
		{
			path_stack.push(node);
			node = crawled_node[node];
		}
		path_stack.push(node);

		while(!path_stack.empty())
		{
			int path_node = path_stack.top();
			path += to_string(path_node)+",";
			path_stack.pop();
		}
		cout << path << endl;
		
	}

	// »Ö¸´É¾³ý±ß
	graph[source][target]  |= delete_edge;

	return path;
}