from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "root"))
session = driver.session()

# get entity
with open('../data/entity2id.txt') as f:
    entitys = []
    line = f.readline()
    while line:
        line = line.strip()
        entity = line.split('	')
        entitys.append(entity)
        line = f.readline()

# insert entity
for name,uid in entitys:
    print('add node in Neo4j %s times and name:%s' % (uid,name))
    insert_query = 'CREATE (a:Entity {name:"%s", uid: %s})' % (name,uid)
    print(insert_query)

    stateResult = session.run(insert_query)
    resultSummary = stateResult.consume()
    print(resultSummary.counters )

# get relation
with open('../data/relation2id.txt') as f:
    relation2id = {}
    line = f.readline()
    while line:
        line = line.strip()
        line = line.split('	')
        relation = line[0]
        id = line[1]

        relation2id[relation] = id
        line = f.readline()

# get relation
with open('../data/train.txt') as f:
    relations = []
    line = f.readline()
    while line:
        line = line.strip()
        relation = line.split('	')
        relations.append(relation)
        line = f.readline()
count = 0
for source, target, relation in relations:
    relation = relation2id[relation]

    print('%d times ' % count)
    count +=1
    insert_query = '''match (a),(b)
                   where a.name='%s' and b.name='%s'
                   create (a)-[:r%s]->(b)
                   ''' % (source,target,relation)
    print(insert_query)

    stateResult = session.run(insert_query)
    resultSummary = stateResult.consume()
    print(resultSummary.counters )


