from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "root"))
session = driver.session()

query = '''MATCH (cs),(ms), p = shortestPath((cs)-[*]->(ms))
           where ID(cs)=%s and ID(ms)=%s
           RETURN p
        '''

id1 = 4581
id2 = 9089

query = query % (str(id1),str(id2))

result = session.run(query)

for record in result:
    print('in first record')
    print(record)

records = result.records()
for record in records:
    print('in second record')
    print(record)

segments = result['records']['_fields']['segments']

for segment in segments:
    start_id = segment['start']['id']
    relation = segment['relationship']['type']
    end_id = segment['end']['id']

    print('(%s,%s,%s)' % (start_id,relation,end_id))