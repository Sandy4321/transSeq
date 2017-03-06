from SQLConnector import *

sqlConn = SqlConnector(db='wds')

# add entity
with open('../data/entity2id.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        line = line.split('	')
        name,id = line[0],line[1]

        sql = 'insert into Entity(id,name) values(%s,"%s")' % (id,name)
        print(sql)

        sqlConn.insert(sql)

        line = f.readline()


# add relationship
with open('../data/relation2id.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        line = line.split('	')
        name,id = line[0],line[1]

        sql = 'insert into Relationship(id,name) values(%s,"%s")' % (id,name)
        print(sql)

        sqlConn.insert(sql)

        line = f.readline()