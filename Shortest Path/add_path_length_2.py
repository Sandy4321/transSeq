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

sqlConn = SqlConnector(db='wds')
sql = 'select id,source,target,relationship from Edge where length = -1;'
result = sqlConn.select(sql)

for i,line in enumerate(result):
    id,source,target,realtionship = line

    if i % 1000 == 0:
        print('now in the %d time' % (i))

    path = get_path(session,source,target)
    if path != None:
        sql = 'update Edge set path="%s",length=2 where id=%s' % (path,id)
        sqlConn.update(sql)


