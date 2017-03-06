from neo4j.v1 import GraphDatabase, basic_auth
# from neo4j.v1.types import Node, Relationship, Path


def get_path(session,source,target):
    query = '''MATCH (cs),(ms), p = shortestPath((cs)-[*]->(ms))
               where ID(cs)=%s and ID(ms)=%s
               RETURN p
            '''
    query = query % (str(source),str(target))
    result = session.run(query)

    for record in result:
        segments = record['p']
        line = []

        for path in segments:
            path_str = '(%s,%s,%s)' % (path.start,path.type,path.end)
            line.append(path_str)

        line = ','.join(line)
        return line
    return None

if __name__ == '__main__':
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "root"))
    session = driver.session()

    id1 = 4581
    id2 = 9089

    print(get_path(session,id1,id2))