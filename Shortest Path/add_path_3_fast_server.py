from SQLConnector import *
from neo4j.v1 import GraphDatabase, basic_auth

def get_path(session,source,target,length=3):
    query = '''
            START s = Node(%s),t=Node(%s)
            MATCH path =(s:Entity)-[*%d..%d]->(t:Entity)
            RETURN path LIMIT 1
            ''' % (source,target,length,length)
    # print(query)

    result = session.run(query)

    for record in result:
        segments = record['path']
        line = []
        s_count = 0
        t_count = 0

        for path in segments:
            path_str = '(%s,%s,%s)' % (path.start,path.type,path.end)
            line.append(path_str)

            if path.start == source or path.end == source:
                s_count += 1
            if path.start == target or path.end == target:
                t_count += 1

        if s_count != 1 or target != 1:
            return None

        line = ','.join(line)
        return line
    return None

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "root"))
session = driver.session()

sqlConn = SqlConnector(db='wds',host='45.32.241.116')
i=0
while True:
    i+=1

    sql = 'select id,source,target,relationship from Edge where length = -1 order by id DESC limit 10;'
    result = sqlConn.select(sql)

    for id,source,target,relation in result:
        print('now in the %d time,(%s,%s,%s) id=%s' % (i,source,target,relation,id))

        try:
            path = get_path(session,source,target)
        except:
            sql = 'update Edge set length=-4 where id=%s' % (id)
            sqlConn.update(sql)
            continue

        if path != None:

            sql = 'update Edge set path="%s",length=3 where id=%s' % (path,id)
            sqlConn.update(sql)
            i += 1
        else:
            sql = 'update Edge set length=-3 where id=%s' % (id)
            sqlConn.update(sql)



