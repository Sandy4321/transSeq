#include <head.h>


byte graph[NODES_TOTAL][NODES_TOTAL];


vector<string> split(string& str,const char* c)
{
    char *cstr, *p;
    vector<string> res;
    cstr = new char[str.size()+1];
    strcpy(cstr,str.c_str());
    p = strtok(cstr,c);
    while(p!=NULL)
    {
        res.push_back(p);
        p = strtok(NULL,c);
    }
    return res;
}

// 图初始化
void init_graph()
{
	for(int i=0;i<NODES_TOTAL;i++)
		for(int j=0;j<NODES_TOTAL;j++)
			graph[i][j]=0;
}

// 构建双向图
int build_bi_graph()
{
	init_graph();

	char *filePath = "D:\\graph\\graph.txt";  
	ifstream file;  
	file.open(filePath,ios::in);  

	if(!file.is_open())  

		return 1;  


	std::string strLine;  
	int i=0;
	while(getline(file,strLine))  
	{  
		if(strLine.empty())  
			continue;  

		vector<string> line = split(strLine,",");
		
		int source = stoi(line[0]);
		int target = stoi(line[1]);


		graph[source][target] |= 0x1;	// 0X1有值 就是顺序边
		graph[target][source] |= 0x2;	// 0X2有值 就是逆序边
		//printf("%d: %d,%d\n",i,source,target);
		i += 1;
	}  

	return 0;
}