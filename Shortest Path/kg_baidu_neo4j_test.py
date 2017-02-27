from neo4j.v1 import GraphDatabase, basic_auth
from SQLConnector import *

# get edge from mysql
print('start get edge from mysql')
sqlConn = SqlConnector(db='kg_baidu')
sql = 'select source,source_type,target,target_type,relation_id from edge;'
result = sqlConn.select(sql)

def get_name(sqlConn,id,type):
    prefix = type
    if type == 'lab_index':
        prefix = 'index'
    elif type == 'laboratory_test':
        prefix = 'test'

    id_ = prefix + '_id'
    name_ = prefix + '_name'


    sql = 'select %s from %s where %s="%s";' % (name_,type,id_,id)
    # print(sql)
    result = sqlConn.select(sql)
    if len(result) == 0:
        return None

    return result[0][0]

node_dict = {}
edge_list = []
for source,source_type,target,target_type,relation_id in result:
    if source not in node_dict:
        name = get_name(sqlConn,source,source_type)
        if name == None:
            continue
        node_dict[source] = (name,source_type)

    if target not in node_dict:
        name = get_name(sqlConn,target,target_type)
        if name == None:
            continue
        node_dict[target] = (name,target_type)

    edge_list.append([source,source_type,target,target_type,relation_id])


# start a neo4j session
print('start start a neo4j session')
driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "root"))
session = driver.session()

# add node in Neo4j
print('start add node in Neo4j')
nodelist = list(node_dict)
for i,node_ in enumerate(nodelist):
    id = node_
    label,type = node_dict[id]
    session.run("CREATE (a:%s {name: {name}, id: {id}})" % type,
               {"name": label, "id": id})
    print('add node in Neo4j %d times and name:%s' % (i,label))

# get relation label from mysql
print('start get relation label from mysql')
relation_id2name = {}
sql = 'select relation_id,relation_name from relation;'
relation_result = sqlConn.select(sql)
for id,name in relation_result:
    relation_id2name[id] = name


# add relation in Neo4j
print('start add relation in Neo4j')
for i,line in enumerate(edge_list):
    source,source_type,target,target_type,relation_id = line
    relation = relation_id2name[relation_id]
    session.run('''match (a),(b)
                   where a.id='%s' and b.id='%s'
                   create (a)-[:%s]->(b)
                   ''' % (source,target,relation))

    print('add relation in Neo4j %d times' % (i))





