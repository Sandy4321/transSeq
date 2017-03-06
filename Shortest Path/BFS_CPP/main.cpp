#include <head.h>
#include <time.h>


int main(void)
{
	//graph = new vector<short>*[NODES_TOTAL];
	//graph_reversed = new vector<short>*[NODES_TOTAL];

	build_bi_graph();

	char *filePath = "D:\\graph\\wds_hcy.txt";  
	ifstream file;  
	file.open(filePath,ios::in);  

	if(!file.is_open())  

		return 1;  

	ofstream out("out_wds_hcy.txt");  

	std::string strLine;  
	int i=0;
	while(getline(file,strLine))  
	{  
		if(strLine.empty())  
			continue; 

		cout << i <<":";
		i+=1;


		vector<string> line = split(strLine,",");
		int source = stoi(line[0]);
		int target = stoi(line[1]);
		int id = stoi(line[2]);

		string path = BFS(source,target,100);
		if(path!="")
		{
			out << id<<","<<path;
		}
		cout<<endl;
	}

	out.close();  
	return 0;
}