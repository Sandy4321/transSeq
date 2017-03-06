
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "root"))
session = driver.session()

def get_path(session,source,target,length):
    query = '''
            START s = Node(%s),t=Node(%s)
            MATCH path =(s:Entity)-[*%d..%d]->(t:Entity)
            WHERE 2 = size(filter(m in nodes(path) where m=s or m=t))
            RETURN path LIMIT 1
            ''' % (source,target,length,length)
    # print(query)

    result = session.run(query)

    for record in result:
        segments = record['path']
        line = []

        for path in segments:
            path_str = '(%s,%s,%s)' % (path.start,path.type,path.end)
            line.append(path_str)

        line = ','.join(line)
        return line
    return None


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
with open('../data/train_not_find_path.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        relation = line.split(',')
        relations.append(relation)
        line = f.readline()

with open('../data/train_with_path_length_3.txt','w') as f:
    noPath = relations
    for length in range(3,4):
        relations = noPath
        noPath = []
        total = len(relations)

        for i,line in enumerate(relations):
            source,target,relation = line[0],line[1],line[2]
            source = name2id[source]
            target = name2id[target]

            try:
                path = get_path(session,source,target,length)
            except:
                path = None

            if path == None:
                noPath.append(line)
            else:
                print('%d times, path is %s' % (i,path))
                f.write(path+'\n')

            if i%1000==0:
                print('step length:%d, %d/%d times' % (length,i,total))



with open('../data/train_length3_not_find_path.txt','w') as f:

    for line in noPath:
        write_line = ','.join(line)
        f.write(write_line+'\n')

