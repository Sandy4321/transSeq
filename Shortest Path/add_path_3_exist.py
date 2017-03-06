import re
from SQLConnector import *
from neo4j.v1 import GraphDatabase, basic_auth
def get_path(session,source,target,length=2):
    query = '''
                MATCH path =(s:Entity)-[*%d..%d]->(t:Entity) WHERE ID(s)=%s and ID(t)=%s RETURN path LIMIT 1
            ''' % (length,length,source,target)

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

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "root"))
session = driver.session()

sqlConn = SqlConnector(db='wds',host='45.32.241.116')

with open('../data/已处理的三路path.txt') as f:
    line = f.readline()
    while line != 'wds':
        # print(line)
        path = re.findall('\(.*\)',line)[0]
        # print(path)

        source = re.findall('(?<=path is \().*?(?=,)',line)[0]
        target = re.findall('(?<=,)[0-9]+?(?=\)\n)',line)[0]

        # print('source:%s ; target:%s' % (source,target))
        sql = 'update Edge set path="%s",length=3 where source=%s and target=%s' % (path,source,target)
        print(sql)
        sqlConn.update(sql)

        line = f.readline()
        # break