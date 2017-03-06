from SQLConnector import *
sqlConn = SqlConnector(db='wds')

sql = 'select source,target,relationship from Edge where type="train";'
# print(sql)
result = sqlConn.select(sql)

node2edge = {}

for source,target,relationship in result:
    # print('%s,%s' % (source,target))
    node2edge[(int(source),int(target))] = "r"+str(relationship)

import csv
def read_csv(filepath):
    results = []
    reader = csv.reader(open(filepath, 'r'))
    for line in reader:
        results.append(line)
    return results

result = read_csv('out_wds_hcy.txt')
for i,line in enumerate(result):
    edge_id = line[0]
    nodes = line[2:]

    path = ''
    start = line[1]
    for end in nodes:
        relation = node2edge[(int(start),int(end))]

        path += '(%s,%s,%s)' % (start,relation,end)
        start=end

    length = path.count('(')
    sql = 'update Edge set length=%d,path="%s" where id=%s' % (length,path,edge_id)
    print(i,":",sql)

    sqlConn.update(sql)



