from shortestPathTest import *
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "root"))
session = driver.session()

name2id = {}
with open('../data/entity2id.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        line = line.split('	')
        name,id = line[0],line[1]
        name2id[name] = id

        line = f.readline()

relations = []
with open('../data/train.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        relation = line.split('	')
        relations.append(relation)
        line = f.readline()

with open('../data/train_with_path.txt','w') as f:
    for i,line in enumerate(relations):
        source,target,relation = line[0],line[1],line[2]
        source = name2id[source]
        target = name2id[target]

        path = get_path(session,source,target)

        print('%d times, path is %s' % (i,path))

        f.write(path+'\n')

