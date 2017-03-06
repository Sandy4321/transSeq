
from SQLConnector import *
sqlConn = SqlConnector(db='wds')

sql = 'select source,target,path,id from Edge where length>0;'
result = sqlConn.select(sql)

for source,target,path,id in result:
    start='(%s,' % source
    end = ',%s)' % target

    if start not in path or end not in path:
        print(id)
