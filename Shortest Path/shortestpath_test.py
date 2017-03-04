from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "root"))
session = driver.session()

id1 = '29fd8d03-bc7d-11e6-abe2-90b11c8ea15c'
id2 = 'fa7d8768-c0fb-11e6-abe2-90b11c8ea15c'



print(session.run('''START a=node(1), b=node(2)
               where a.id='%s' and b.id='%s
               MATCH p = shortestPath( a-[*..15]->b )
               RETURN p''' % (id1,id2)))