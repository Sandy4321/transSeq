import csv

entity2id = {}
with open('../data/entity2id.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        line = line.split('	')
        name,id = line
        entity2id[name] = id

        line = f.readline()

graph = []
with open('../data/train.txt') as f:
    line = f.readline()
    while line:
        line = line.strip()
        line = line.split('	')
        s,t,relation = line

        s = entity2id[s]
        t = entity2id[t]

        graph.append([s,t])

        line = f.readline()

def write_csv(filepath,lines):
    writer = csv.writer(open(filepath, 'w',encoding='utf-8',newline=''))
    for line in lines:
        writer.writerow(line)

write_csv('graph.txt',graph)

