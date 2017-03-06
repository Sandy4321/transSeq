from SQLConnector import *

sqlConn = SqlConnector(db='wds')
# add entity
entity2id = {}
with open('../data/entity2id.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        line = line.split('	')
        name,id = line[0],line[1]
        entity2id[name] = id

        line = f.readline()

relation2id = {}
# add relationship
with open('../data/relation2id.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        line = line.split('	')
        name,id = line[0],line[1]
        relation2id[name] = id

        line = f.readline()

# train
with open('../data/train.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        line = line.split('	')
        source,target,relationship = line[0],line[1],line[2]
        source = entity2id[source]
        target = entity2id[target]
        relationship = relation2id[relationship]

        sql = 'insert into Edge(source,target,relationship,type) values(%s,%s,%s,"train")' % (source,target,relationship)
        print(sql)
        sqlConn.insert(sql)

        line = f.readline()

# test
with open('../data/test.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        line = line.split('	')
        source,target,relationship = line[0],line[1],line[2]
        source = entity2id[source]
        target = entity2id[target]
        relationship = relation2id[relationship]

        sql = 'insert into Edge(source,target,relationship,type) values(%s,%s,%s,"test")' % (source,target,relationship)
        print(sql)
        sqlConn.insert(sql)

        line = f.readline()

# valid
with open('../data/valid.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        line = line.split('	')
        source,target,relationship = line[0],line[1],line[2]
        source = entity2id[source]
        target = entity2id[target]
        relationship = relation2id[relationship]

        sql = 'insert into Edge(source,target,relationship,type) values(%s,%s,%s,"valid")' % (source,target,relationship)
        print(sql)
        sqlConn.insert(sql)

        line = f.readline()