from SQLConnector import *
sqlConn = SqlConnector(db='wds')

sql = 'select source,target,id from Edge where length<0;'
result = sqlConn.select(sql)

import csv

def write_csv(filepath,lines):
    writer = csv.writer(open(filepath, 'w',encoding='utf-8'))
    for line in lines:
        writer.writerow(line)

write_csv('wds_hcy.txt',result)
