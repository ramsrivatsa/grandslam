from collections import defaultdict
import json
import numpy as np

class MicroService:
    def __init__(self, microservice_dict,name, bmax, iprange, alias):
        self.microservice_dict      = microservice_dict
        self.name                   = name
        self.bmax                   = bmax
        self.iprange                = iprange
        self.alias                = alias
    microservice_data_dict = defaultdict(lambda  : defaultdict(list))
    num_queries = 0
    input_size = 999
    queries = []
    num_instances = 1

####### Common data structures #########
list_microservice = []


####### Temp data structures #########
service_data = defaultdict( lambda: defaultdict(lambda: defaultdict( list )))
service_mean = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
service_std = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))

####### Microservice Information #########
'''
    Automatic Speech Recognition = AA
'''

## Simulator Data
aa = defaultdict(lambda  : defaultdict(int))
brange = 16
ilist = [54]

## parse data
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/paper-results/services/ASR/latency.txt').readlines()]

for item in fList:
    #print item
    if 'batch size' in item:
        bsize = int(item.split('batch size ')[1].split(' ')[0])
        isize = int(item.split('batch size ')[1].split(' ')[3].split('.')[0])
    elif 'ASR' in item:
        appname = 'asr'
    else:
        #print item
        service_data[appname][bsize][isize].append(float(item.split()[2].split(':')[1]))

for x,a in service_data.iteritems():
    for y,b in service_data[x].iteritems():
        for z,c in service_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in service_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            service_mean[x][y][z] = np.median(temp_list)
            service_std[x][y][z] = np.std(temp_list)

for x in range(1, brange+1):
    for y in ilist:
        aa[x][y] = service_mean['asr'][x][y]
AA      =   MicroService(aa,'AA', brange, ilist, 'asr')
AA.microservice_data_dict = service_data['asr']
list_microservice.append(AA)
#print(json.dumps(service_data['asr'], indent = 4))

#print service_data
service_data.clear()
service_mean.clear()
service_std.clear()
#print service_data

'''
    Natural Language Understanding = BB
'''
## Simulator Data
bb = defaultdict(lambda  : defaultdict(int))
brange = 128
ilist = list(np.arange(2,58))
ilist.append(59)
ilist.append(60)
ilist.append(61)
ilist.append(63)
ilist.append(70)

fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/paper-results/services/NLU/latency.txt').readlines()]

for item in fList:
    #print item
    if 'batch size' in item:
        bsize = int(item.split('batch size ')[1].split(' ')[0])
        isize = int(item.split('batch size ')[1].split(' ')[3].split('.')[0])
    elif 'POS' in item:
        appname = 'pos'
    elif 'CHK' in item:
        appname = 'chk'
    elif 'NER' in item:
        appname = 'ner'
    else:
        service_data[appname][bsize][isize].append(float(item.split()[2].split(':')[1]))

for x,a in service_data.iteritems():
    for y,b in service_data[x].iteritems():
        for z,c in service_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in service_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            del temp_list[0]
            del temp_list[1]
            del temp_list[len(temp_list)-1]
            del temp_list[len(temp_list)-1]
            #print temp_list
            service_mean[x][y][z] = np.mean(temp_list)
            service_std[x][y][z] = np.std(temp_list)

for x in range(1, brange+1):
    for y in ilist:
        bb[x][y] = service_mean['pos'][x][y] + service_mean['chk'][x][y] +  service_mean['ner'][x][y]
BB      =   MicroService(bb, 'BB', brange, ilist, 'nlu')
BB.microservice_data_dict = bb
list_microservice.append(BB)

service_data.clear()
service_mean.clear()
service_std.clear()

'''
     Question Answering System = CC
'''
## Simulator Data
cc = defaultdict(lambda  : defaultdict(int))
brange = 128
ilist = list(np.arange(1,5))

#Parse data
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/isca-results/services/cpu/QA/latency.txt').readlines()]
#fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/paper-results/services/QA/latency.txt').readlines()]

appname = 'qa'
for item in fList:
    #print item
    if 'batch size' in item:
        bsize = int(item.split('batch size - ')[1])
        isize = int(item.split('input - ')[1].split(' ')[0])
    elif 'Latency' in item:
        service_data[appname][bsize][isize].append(float(item.split('Latency - ')[1]))


for x,a in service_data.iteritems():
    for y,b in service_data[x].iteritems():
        for z,c in service_data[x][y].iteritems():
            temp_list = []
            for item in service_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            del temp_list[0]
            del temp_list[1]
            del temp_list[len(temp_list)-1]
            del temp_list[len(temp_list)-1]
            service_mean[x][y][z] = np.mean(temp_list)
            service_std[x][y][z] = np.std(temp_list)

for x in range(1, brange+1):
    for y in ilist:
        cc[x][y] = service_mean['qa'][x][y]
CC      =   MicroService(cc, 'CC', brange, ilist, 'qa')
CC.microservice_data_dict = service_data['qa']
list_microservice.append(CC)

service_data.clear()
service_mean.clear()
service_std.clear()

'''
     Image Classification = PP
'''
## Simulator Data
pp = defaultdict(lambda  : defaultdict(int))
brange = 64
ilist = [64, 128, 256]
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/isca-results/services/cpu/IMC/latency.txt').readlines()]

appname = 'imc'
for item in fList:
    #print item
    if 'Batch Size ' in item:
        bsize = int(item.split('Batch Size ')[1].split(' ')[0])
        isize = int(item.split('Input Size ')[1].split(' ')[0])
    else:
        service_data[appname][bsize][isize].append(float(item.split(" - ")[1].split(" ")[0]))

for x,a in service_data.iteritems():
    for y,b in service_data[x].iteritems():
        for z,c in service_data[x][y].iteritems():
            temp_list = []
            for item in service_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            service_mean[x][y][z] = np.median(temp_list)
            service_std[x][y][z] = np.std(temp_list)

#print service_mean['imc'][128]

for x in range(1, brange+1):
    for y in ilist:
        pp[x][y] = service_mean['imc'][x][y]
PP      =   MicroService(pp, 'PP', brange, ilist, 'imc')
PP.microservice_data_dict = service_data['imc']
list_microservice.append(PP)


'''
    Text To Speech = QQ
'''

## Simulator Data
qq = defaultdict(lambda  : defaultdict(int))
brange = 16
ilist = [54]


for x in range(1, brange+1):
    for y in ilist:
        qq[x][y] =aa[x][y]
QQ      =   MicroService(qq, 'QQ', brange, ilist, 'tts')
#print type(QQ.microservice_dict[1][54])
QQ.microservice_data_dict = AA.microservice_data_dict
list_microservice.append(QQ)

service_data.clear()
service_mean.clear()
service_std.clear()


'''
     Activity Pose = DD
'''
## Simulator Data
dd = defaultdict(lambda  : defaultdict(int))
brange = 64
ilist = [64, 128, 256]
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/isca-results/services/cpu/activity-pose/latency.txt').readlines()]

appname = 'ap'
for item in fList:
    #print item
    if 'Batch Size ' in item:
        bsize = int(item.split('Batch Size ')[1].split(' ')[0])
        isize = int(item.split('Input Size ')[1].split(' ')[0])
    else:
        service_data[appname][bsize][isize].append(float(item.split(" - ")[1].split(" ")[0]))

for x,a in service_data.iteritems():
    for y,b in service_data[x].iteritems():
        for z,c in service_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in service_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            service_mean[x][y][z] = 1000*(np.median(temp_list))
            service_std[x][y][z] = np.std(temp_list)


for x in range(1, brange+1):
    for y in ilist:
        dd[x][y] = service_mean['ap'][x][y]
DD      =   MicroService(dd, 'DD', brange, ilist, 'ap')
DD.microservice_data_dict = service_data['ap']
list_microservice.append(DD)

service_data.clear()
service_mean.clear()
service_std.clear()


'''
     FACE DETECTION  = EE
'''
## Simulator Data
ee = defaultdict(lambda  : defaultdict(int))
brange = 64
ilist = [64, 128, 256]
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/isca-results/services/cpu/face-detect/latency.txt').readlines()]

appname = 'faced'
for item in fList:
    #print item
    if 'Batch Size ' in item:
        bsize = int(item.split('Batch Size ')[1].split(' ')[0])
        isize = int(item.split('Input Size ')[1].split(' ')[0])
    else:
        service_data[appname][bsize][isize].append(float(item.split(" - ")[1].split(" ")[0]))

for x,a in service_data.iteritems():
    for y,b in service_data[x].iteritems():
        for z,c in service_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in service_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            service_mean[x][y][z] = np.median(temp_list)
            service_std[x][y][z] = np.std(temp_list)


for x in range(1, brange+1):
    for y in ilist:
        ee[x][y] = service_mean['faced'][x][y]
EE      =   MicroService(ee, 'EE', brange, ilist, 'faced')
EE.microservice_data_dict = service_data['faced']
list_microservice.append(EE)

service_data.clear()
service_mean.clear()
service_std.clear()


'''
     FACE RECOGNITION  = FF
'''
## Simulator Data
ff = defaultdict(lambda  : defaultdict(int))
brange = 64
ilist = [64, 128, 256]
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/isca-results/services/cpu/face-recognition/latency.txt').readlines()]

appname = 'facer'
for item in fList:
    #print item
    if 'Batch Size ' in item:
        bsize = int(item.split('Batch Size ')[1].split(' ')[0])
        isize = int(item.split('Input Size ')[1].split(' ')[0])
    else:
        service_data[appname][bsize][isize].append(float(item.split(" - ")[1].split(" ")[0]))

for x,a in service_data.iteritems():
    for y,b in service_data[x].iteritems():
        for z,c in service_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in service_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            service_mean[x][y][z] = np.median(temp_list)
            service_std[x][y][z] = np.std(temp_list)


for x in range(1, brange+1):
    for y in ilist:
        ff[x][y] = service_mean['facer'][x][y]
FF      =   MicroService(ff, 'FF', brange, ilist, 'facerec')
FF.microservice_data_dict = service_data['facer']
list_microservice.append(FF)

service_data.clear()
service_mean.clear()
service_std.clear()


'''
     HUMAN SEGMENTATION  = GG
'''
## Simulator Data
gg = defaultdict(lambda  : defaultdict(int))
brange = 32
ilist = [64, 128]
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/isca-results/services/cpu/human-segmentation/latency.txt').readlines()]

appname = 'hs'
for item in fList:
    if 'Batch Size ' in item:
        bsize = int(item.split('Batch Size ')[1].split(' ')[0])
        isize = int(item.split('Input Size ')[1].split(' ')[0])
    else:
        service_data[appname][bsize][isize].append(float(item.split(" - ")[1].split(" ")[0]))

for x,a in service_data.iteritems():
    for y,b in service_data[x].iteritems():
        for z,c in service_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in service_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            service_mean[x][y][z] = np.median(temp_list)
            service_std[x][y][z] = np.std(temp_list)


for x in range(1, brange+1):
    for y in ilist:
        gg[x][y] = service_mean['hs'][x][y]
GG      =   MicroService(gg, 'GG', brange, ilist, 'hs')
GG.microservice_data_dict = service_data['hs']
list_microservice.append(GG)

service_data.clear()
service_mean.clear()
service_std.clear()


'''
     YCSB - NOSQL  = HH
'''
## Simulator Data
hh = defaultdict(lambda  : defaultdict(int))
brange = 128
ilist = [1]
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/isca-results/services/cpu/human-segmentation/latency.txt').readlines()]

appname = 'ycsb'
for x in xrange(1,129):
    #print x
    fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/isca-results/services/cpu/ycsb/outputfile_%s.res'%x).readlines()]
    for item in fList[1:len(fList)]:
        #print item.split(',')[len(item.split(','))-3]
        service_data[appname][1][x].append(float(item.split(',')[len(item.split(','))-3]))
     #print np.mean(ycsb_data[x])

for item in xrange(1,129):
     #temp_list.append(imc_mean['imc'][item][128])
     #print np.mean(ycsb_data[item])
     service_mean[appname][1][item] = np.mean(service_data[appname][1][item])
     service_std[appname][1][item] = np.std(service_data[appname][1][item])

for x in range(1, brange+1):
    for y in ilist:
        hh[x][y] = service_mean['ycsb'][x][y]
HH      =   MicroService(hh, 'HH', brange, ilist, 'ycsb')
HH.microservice_data_dict = service_data['ycsb']
list_microservice.append(HH)

service_data.clear()
service_mean.clear()
service_std.clear()

#print CC.microservice_dict

AA.input_size = 54      #Automatic Speech Recognition
BB.input_size = 70      #Natural Language Understanding
CC.input_size = 4       #Question Answering System
PP.input_size = 128     #Image Classification
QQ.input_size = 54      #Text To Speech
DD.input_size = 128     #Activity Pose
EE.input_size = 128     #Face Detection
FF.input_size = 128     #Face Recognition
GG.input_size = 64      #Human Segmentation
HH.input_size = 1       #YCSB


#for idx,item in enumerate(list_microservice):
#    print item.name, item.bmax, item.iprange, item.num_queries, item.input_size
#    if idx == 8:
#        print item.name, item.bmax, item.iprange, item.num_queries, item.input_size
#        print(json.dumps(item.microservice_dict, indent = 4))
#        print(json.dumps(item.microservice_data_dict, indent = 4))


