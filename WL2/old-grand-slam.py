from collections import defaultdict
import json
import pandas as pd
import numpy as np
import itertools
import sys
import bisect
from stackedBarGraph import StackedBarGrapher
SBG = StackedBarGrapher()
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as cl
import matplotlib.pyplot as pl
# List of microservices and timing


#batch_size=11                                       #10
#input_size=6                                        #5
#
#for x in range(1, batch_size):
#    for y in range(1, batch_size):
#        AA[x][y] = 0.1 + 0.01*x*y
#        BB[x][y] = 0.2 + 0.01*x*y
#        CC[x][y] = 0.3 + 0.01*x*y
#        PP[x][y] = 0.4 + 0.01*x*y
#        QQ[x][y] = 0.5 + 0.01*x*y
#


class MicroService:
    #microservice = defaultdict(lambda  : defaultdict(int))
    queries = []
    def __init__(self, microservice_dict,name, bmax, iprange):
        self.microservice_dict      = microservice_dict
        self.name                   = name
        self.bmax                   = bmax
        self.iprange                = iprange
    microservice_list_dict = defaultdict(lambda  : defaultdict(list))
    num_queries = 0
    input_size = 999
    #num_instances = 1
    state = []

class Query:
    def __init__(self, userid, batchsize, order, queryid, dag,sla):
        self.userid         = userid
        self.batch_size     = batchsize
        self.order          = order
        self.queryid        = queryid
        self.dag            = dag
        self.sla            = sla
    single_time             = 0     #should reset
    slack_value             = 0
    elapsed_time            = 0
    forward_time            = 0


class UserInfo:
    def __init__(self, sla, freq, dag, userid):
        self.sla    = sla
        self.freq   = freq
        self.dag    = dag
        self.userid = userid

def isSafe(list_users, list_microservice):
    for user in list_users:
        # Constraint on having only 2 characters per microservice:
        check_service = user.dag[len(user.dag)-2:len(user.dag)]
        #print check_service
        for service in list_microservice:
            #print service.name, check_service
            if service.name == check_service:
                for que in service.queries:
                    print service.name, que.userid, que.queryid, que.elapsed_time, que.sla
                    if que.sla < que.elapsed_time:
                        return False

    return True


def decompose(n):
    try:
        return q[n]
    except:
        pass

    result = [[n]]

    for i in range(1, n):
        a = n-i
        R = decompose(i)
        for r in R:
            if r[0] <= a:
                result.append([a] + r)

    q[n] = result
    return result


def state_ordering(string1, string2):
    ### Iterating by two
    list1 = []
    for i in xrange(0,len(string1),2):
        op, code = string1[i:i+2]
        list1.append(op+code)
    list2 = []
    for i in xrange(0,len(string2),2):
        op, code = string2[i:i+2]
        list2.append(op+code)

    common_list = []
    for item in list1:
        if item in list2:
            common_list.append(item)

    order_list = []
    prev_id1 = len(list1)
    prev_id2 = len(list2)
    for idx, item in reversed(list(enumerate(common_list))):
        #print idx,item
        id1 = list1.index(item)
        id2 = list2.index(item)
        #print list1[id1+1:prev_id1]
        #print list2[id2+1:prev_id2]
        for temp_item in list1[id1+1:prev_id1]:
            #print temp_item
            order_list.append(temp_item)
        for temp_item in list2[id2+1:prev_id2]:
            #print temp_item
            order_list.append(temp_item)
        order_list.append(item)
        prev_id1 = id1
        prev_id2 = id2

    for temp_item in list1[0:prev_id1]:
        #print temp_item
        order_list.append(temp_item)
    for temp_item in list2[0:prev_id2]:
        #print temp_item
        order_list.append(temp_item)
    return order_list

####### Microservice Information #########
'''
    Automatic Speech Recognition = AA
'''

## Simulator Data
aa = defaultdict(lambda  : defaultdict(int))
brange = 16
ilist = [54]

## parse data
list_microservice = []
asr_data = defaultdict( lambda: defaultdict(lambda: defaultdict( list )))
asr_mean = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
asr_std = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
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
        asr_data[appname][bsize][isize].append(float(item.split()[2].split(':')[1]))

for x,a in asr_data.iteritems():
    for y,b in asr_data[x].iteritems():
        for z,c in asr_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in asr_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            #del temp_list[0]
            #del temp_list[1]
            #del temp_list[len(temp_list)-1]
            #del temp_list[len(temp_list)-1]
            #print temp_list
            asr_mean[x][y][z] = np.median(temp_list)
            asr_std[x][y][z] = np.std(temp_list)

for x in range(1, brange+1):
    for y in ilist:
        aa[x][y] = asr_mean['asr'][x][y]
AA      =   MicroService(aa,'AA', brange, ilist)
AA.microservice_list_dict = asr_data['asr']
list_microservice.append(AA)
#print(json.dumps(asr_data['asr'], indent = 4))


'''
    Natural Language Understanding = BB
'''
## Simulator Data
temp_nlp_data = defaultdict(lambda  : defaultdict(int))
bb = defaultdict(lambda  : defaultdict(int))
brange = 128
ilist = list(np.arange(2,58))
ilist.append(59)
ilist.append(60)
ilist.append(61)
ilist.append(63)
ilist.append(70)

#Parse data
temp_nlp_data = defaultdict(lambda  : defaultdict(int))
nlp_data = defaultdict( lambda: defaultdict(lambda: defaultdict( list )))
nlp_mean = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
nlp_std = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
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
        nlp_data[appname][bsize][isize].append(float(item.split()[2].split(':')[1]))

for x,a in nlp_data.iteritems():
    for y,b in nlp_data[x].iteritems():
        for z,c in nlp_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in nlp_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            del temp_list[0]
            del temp_list[1]
            del temp_list[len(temp_list)-1]
            del temp_list[len(temp_list)-1]
            #print temp_list
            nlp_mean[x][y][z] = np.mean(temp_list)
            nlp_std[x][y][z] = np.std(temp_list)

for x in range(1, brange+1):
    for y in ilist:
        bb[x][y] = nlp_mean['pos'][x][y] + nlp_mean['chk'][x][y] +  nlp_mean['ner'][x][y]
BB      =   MicroService(bb, 'BB', brange, ilist)
BB.microservice_list_dict = bb
list_microservice.append(BB)
print(json.dumps(bb, indent = 4))
#print bb[100][70], nlp_mean['pos'][100][70], nlp_mean['chk'][100][70], nlp_mean['ner'][100][70]

'''
     Question Answering System = CC
'''
## Simulator Data
cc = defaultdict(lambda  : defaultdict(int))
brange = 128
ilist = list(np.arange(1,6))

#Parse data
qa_data = defaultdict( lambda: defaultdict(lambda: defaultdict( list )))
qa_mean = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
qa_std = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/paper-results/services/QA/latency.txt').readlines()]

appname = 'qa'
for item in fList:
    #print item
    if 'batch size' in item:
        bsize = int(item.split('batch size - ')[1])
        isize = int(item.split('input - ')[1].split(' ')[0])
    elif 'Latency' in item:
        qa_data[appname][bsize][isize].append(float(item.split('Latency - ')[1]))


for x,a in qa_data.iteritems():
    for y,b in qa_data[x].iteritems():
        for z,c in qa_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in qa_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            del temp_list[0]
            del temp_list[1]
            del temp_list[len(temp_list)-1]
            del temp_list[len(temp_list)-1]
            #print temp_list
            qa_mean[x][y][z] = np.mean(temp_list)
            qa_std[x][y][z] = np.std(temp_list)

for x in range(1, brange+1):
    for y in ilist:
        cc[x][y] = qa_mean['qa'][x][y]
CC      =   MicroService(cc, 'CC', brange, ilist)
CC.microservice_list_dict = qa_data['qa']
#print CC.microservice_dict[10][1]
list_microservice.append(CC)


'''
     Image Classification = PP
'''
## Simulator Data
pp = defaultdict(lambda  : defaultdict(int))
brange = 16
ilist = [64, 128, 256]
imc_data = defaultdict( lambda: defaultdict(lambda: defaultdict( list )))
imc_mean = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
imc_std = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/paper-results/services/IMC/latency.txt').readlines()]

appname = 'imc'
for item in fList:
    #print item
    if 'Batch Size ' in item:
        bsize = int(item.split('Batch Size ')[1].split(' ')[0])
        isize = int(item.split('Input Size ')[1].split(' ')[0])
    else:
        imc_data[appname][bsize][isize].append(float(item.split(" - ")[1].split(" ")[0]))

for x,a in imc_data.iteritems():
    for y,b in imc_data[x].iteritems():
        for z,c in imc_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in imc_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            #del temp_list[0]
            #del temp_list[1]
            #del temp_list[len(temp_list)-1]
            #del temp_list[len(temp_list)-1]
            #print temp_list
            imc_mean[x][y][z] = np.median(temp_list)
            imc_std[x][y][z] = np.std(temp_list)
#print imc_mean['imc'][128][64]
for x in range(1, brange+1):
    for y in ilist:
        pp[x][y] = imc_mean['imc'][x][y]
PP      =   MicroService(pp, 'PP', brange, ilist)
PP.microservice_list_dict = imc_data['imc']
list_microservice.append(PP)
#print PP.microservice_dict[10][64]
#print PP.microservice_dict[10][128]
#print PP.microservice_dict[10][256]

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
QQ      =   MicroService(qq, 'QQ', brange, ilist)
#print type(QQ.microservice_dict[1][54])
QQ.microservice_list_dict = asr_data['asr']
list_microservice.append(QQ)



'''
     Activity Pose = DD
'''
## Simulator Data
dd = defaultdict(lambda  : defaultdict(int))
brange = 16
ilist = [64, 128, 256]
ap_data = defaultdict( lambda: defaultdict(lambda: defaultdict( list )))
ap_mean = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
ap_std = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/paper-results/services/activity-pose/latency.txt').readlines()]

appname = 'ap'
for item in fList:
    #print item
    if 'Batch Size ' in item:
        bsize = int(item.split('Batch Size ')[1].split(' ')[0])
        isize = int(item.split('Input Size ')[1].split(' ')[0])
    else:
        ap_data[appname][bsize][isize].append(float(item.split(" - ")[1].split(" ")[0]))

for x,a in ap_data.iteritems():
    for y,b in ap_data[x].iteritems():
        for z,c in ap_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in ap_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            #del temp_list[0]
            #del temp_list[1]
            #del temp_list[len(temp_list)-1]
            #del temp_list[len(temp_list)-1]
            #print temp_list
            ap_mean[x][y][z] = 1000*(np.median(temp_list))
            ap_std[x][y][z] = np.std(temp_list)
#print ap_mean['ap'][128][64]
for x in range(1, brange+1):
    for y in ilist:
        dd[x][y] = ap_mean['ap'][x][y]
DD      =   MicroService(dd, 'DD', brange, ilist)
DD.microservice_list_dict = ap_data['ap']
list_microservice.append(DD)
#print DD.microservice_dict[10][128]
#print PP.microservice_dict[10][64]
#print PP.microservice_dict[10][128]
#print PP.microservice_dict[10][256]



'''
     FACE DETECTION  = EE
'''
## Simulator Data
ee = defaultdict(lambda  : defaultdict(int))
brange = 16
ilist = [64, 128, 256]
faced_data = defaultdict( lambda: defaultdict(lambda: defaultdict( list )))
faced_mean = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
faced_std = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/paper-results/services/face-detect/latency.txt').readlines()]

appname = 'faced'
for item in fList:
    #print item
    if 'Batch Size ' in item:
        bsize = int(item.split('Batch Size ')[1].split(' ')[0])
        isize = int(item.split('Input Size ')[1].split(' ')[0])
    else:
        faced_data[appname][bsize][isize].append(float(item.split(" - ")[1].split(" ")[0]))

for x,a in faced_data.iteritems():
    for y,b in faced_data[x].iteritems():
        for z,c in faced_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in faced_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            #del temp_list[0]
            #del temp_list[1]
            #del temp_list[len(temp_list)-1]
            #del temp_list[len(temp_list)-1]
            #print temp_list
            faced_mean[x][y][z] = np.median(temp_list)
            faced_std[x][y][z] = np.std(temp_list)
#print faced_mean['faced'][128][64]
for x in range(1, brange+1):
    for y in ilist:
        ee[x][y] = faced_mean['faced'][x][y]
EE      =   MicroService(ee, 'EE', brange, ilist)
EE.microservice_list_dict = faced_data['faced']
list_microservice.append(EE)
#print EE.microservice_dict[10][128]
#print PP.microservice_dict[10][64]
#print PP.microservice_dict[10][128]
#print PP.microservice_dict[10][256]

'''
     FACE RECOGNITION  = FF
'''
## Simulator Data
ff = defaultdict(lambda  : defaultdict(int))
brange = 16
ilist = [64, 128, 256]
facer_data = defaultdict( lambda: defaultdict(lambda: defaultdict( list )))
facer_mean = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
facer_std = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/paper-results/services/face-recognition/latency.txt').readlines()]

appname = 'facer'
for item in fList:
    #print item
    if 'Batch Size ' in item:
        bsize = int(item.split('Batch Size ')[1].split(' ')[0])
        isize = int(item.split('Input Size ')[1].split(' ')[0])
    else:
        facer_data[appname][bsize][isize].append(float(item.split(" - ")[1].split(" ")[0]))

for x,a in facer_data.iteritems():
    for y,b in facer_data[x].iteritems():
        for z,c in facer_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in facer_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            #del temp_list[0]
            #del temp_list[1]
            #del temp_list[len(temp_list)-1]
            #del temp_list[len(temp_list)-1]
            #print temp_list
            facer_mean[x][y][z] = np.median(temp_list)
            facer_std[x][y][z] = np.std(temp_list)
#print facer_mean['facer'][128][64]
for x in range(1, brange+1):
    for y in ilist:
        ff[x][y] = facer_mean['facer'][x][y]
FF      =   MicroService(ff, 'FF', brange, ilist)
FF.microservice_list_dict = facer_data['facer']
list_microservice.append(FF)


'''
     HUMAN SEGMENTATION  = GG
'''
## Simulator Data
gg = defaultdict(lambda  : defaultdict(int))
brange = 16
ilist = [64, 128, 256]
hs_data = defaultdict( lambda: defaultdict(lambda: defaultdict( list )))
hs_mean = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
hs_std = defaultdict( lambda: defaultdict(lambda: defaultdict( float )))
fList = [s.strip() for s in open('/home/ram/api-as-service/grand-slam/paper-results/services/face-recognition/latency.txt').readlines()]

appname = 'hs'
for item in fList:
    #print item
    if 'Batch Size ' in item:
        bsize = int(item.split('Batch Size ')[1].split(' ')[0])
        isize = int(item.split('Input Size ')[1].split(' ')[0])
    else:
        hs_data[appname][bsize][isize].append(float(item.split(" - ")[1].split(" ")[0]))

for x,a in hs_data.iteritems():
    for y,b in hs_data[x].iteritems():
        for z,c in hs_data[x][y].iteritems():
            #print x,y,z
            temp_list = []
            for item in hs_data[x][y][z]:
                temp_list.append(item)
            temp_list.sort()
            #del temp_list[0]
            #del temp_list[1]
            #del temp_list[len(temp_list)-1]
            #del temp_list[len(temp_list)-1]
            #print temp_list
            hs_mean[x][y][z] = np.median(temp_list)
            hs_std[x][y][z] = np.std(temp_list)
#print hs_mean['hs'][128][64]
for x in range(1, brange+1):
    for y in ilist:
        gg[x][y] = hs_mean['hs'][x][y]
GG      =   MicroService(gg, 'GG', brange, ilist)
GG.microservice_list_dict = hs_data['hs']
list_microservice.append(GG)
#print PP.microservice_dict[10][64]
#print PP.microservice_dict[10][128]
#print PP.microservice_dict[10][256]


######### User Information ###############
num_user = 2                                        # number of users
list_users = []                                     # list of users

#sla,freq,dag
#user1           = UserInfo(1300, 250,'AABBCC','user1')
#user1           = UserInfo(1300, 200,'DDBBCC','user1')
user1           = UserInfo(1300, 100,'EEFFCC','user1')
list_users.append(user1)

user2       = UserInfo(1800, 100,'PPBBCCQQ', 'user2')
#user2       = UserInfo(1800, 200,'GGDDEEFF', 'user2')
list_users.append(user2)


######### microservice input-size Information ###############
AA.input_size = 54
BB.input_size = 70
CC.input_size = 1
PP.input_size = 128
QQ.input_size = 54
DD.input_size = 128
EE.input_size = 128
FF.input_size = 128
GG.input_size = 64

#state_ordering = []
microservice_ordering = state_ordering(user1.dag,user2.dag)
microservice_ordering = microservice_ordering[::-1]
#print microservice_ordering

#initiating all microservices
for service in list_microservice:
    #print service.name
    temp_queries = []
    for user in list_users:
        if service.name in user.dag:
            #print service.name,user.dag
            service.num_queries = service.num_queries + user.freq
            for que in xrange(0,user.freq):
                #print service.name
                #print que+1
                q = Query(user.userid, 99, 99, que+1, user.dag, user.sla)
                temp_queries.append(q)
                del q
    service.queries = temp_queries
    del temp_queries
    #print '-------------'

## Old state space calculation
 # Iterate through state spaces
#input_size = 2
max_batch_size = 16
#print len(list_state_space)
#print CC.microservice_dict[128][5]
#sys.exit(0)
for idx_service, service in enumerate(microservice_ordering):
    #print service
    for service_twice in list_microservice:
        if service_twice.name == service:
            #print service, service_twice.name, service_twice.input_size, QQ.microservice_dict[1][service_twice.input_size]
            for que in service_twice.queries:
                #temp_dag_single = service + que.dag.split(service)[1]
                prev_forward_time = 0
                single_time = 0
                curr_single_time = 0

                for service_thrice in list_microservice:
                    if service_thrice.name in que.dag:
                        que.single_time = que.single_time + \
                        service_thrice.microservice_dict[1][service_thrice.input_size]
                        #print service_thrice.microservice_dict[1] \
                        #        [service_thrice.input_size], service_thrice.name, service_thrice.input_size
                    if service_thrice.name == service_twice.name:
                        curr_single_time = service_thrice.microservice_dict[1][service_thrice.input_size]


                if que.dag.split(service_twice.name)[0] == '':
                    prev_stage_elapsed = None
                else:
                    #delim_elapsed = len(que.dag.split(service_twice.name)[0])
                    #print 'coming here'
                    #print que.dag.split(service_twice.name)[0], delim_elapsed
                    prev_stage_elapsed = que.dag.split(service_twice.name)[0][-2:]

                #print prev_stage_elapsed
                if prev_stage_elapsed != None:
                    for service_five in list_microservice:
                        if service_five.name in prev_stage_elapsed:
                            for que3 in service_five.queries:
                                if que3.userid == que.userid and que3.queryid == que.queryid:
                                    prev_forward_time = que3.forward_time
                else:
                    prev_forward_time = 0
                #print prev_forward_time
                #print service_thrice.input_size, curr_single_time, service_thrice.microservice_dict[1][service_thrice.input_size], prev_forward_time
                expected_time = ((float(curr_single_time)/que.single_time) * que.sla) + prev_forward_time
                #print que.userid, que.queryid, que.single_time, \
                #        curr_single_time, expected_time, service_twice.bmax, \
                #        prev_forward_time
                que.slack_value = expected_time
            sorted_queries = sorted(service_twice.queries, key=lambda que: que.slack_value )

            #print len(sorted_queries)
            micro_list = []
            for item in xrange(1,service_twice.bmax+1):
                micro_list.append(service_twice.microservice_dict[item][service_twice.input_size])
            #print micro_list

            #index = bisect.bisect(micro_list, que.slack_value)
            #if len(service_twice.queries) < index:
            #    index = len(service_twice.queries)
            #else:
            #    num_queries = index
            #    cumilative_latency = service_twice.microservice_dict[index][service_twice.input_size]
            #new_index = index
            #print '*********Starting trouble**********'

            temp_query_list = sorted_queries
            num_instances = 1
            cut_lim = 1
            increase = True
            while increase == True:
                delim_list = []
                query_timing = []
                ind_queries = []
                max_queries = len(temp_query_list)
                cut_lim = cut_lim + 1
                #for jus_print in temp_query_list:
                #    print jus_print.userid, jus_print.queryid
                #print 'watch out for here'
                #print max_queries
                num_queries = 0
                start_queries=0
                cumilative_slack = 0
                split_slack = temp_query_list[0].slack_value
                #print sort_new_que.userid, sort_new_que.queryid
                while (num_queries < len(temp_query_list)):
                    # Bisecting the sorted query list with lowest slack
                    temp_index = bisect.bisect(micro_list, split_slack)
                    #print '3*'
                    #print start_queries, temp_index, split_slack, micro_list[temp_index-1]
                    if ( temp_index >= max_queries ):
                        temp_index = max_queries
                    num_queries = num_queries + temp_index
                    max_queries = max_queries - temp_index
                    start_queries = start_queries + temp_index

                    if start_queries < len(temp_query_list):
                        #account for queuing - cumulative slack is the slack for queuing
                        cumilative_slack = cumilative_slack + micro_list[temp_index-1]
                        split_slack = sorted_queries[start_queries].slack_value -\
                                cumilative_slack
                        if split_slack <= micro_list[0]:
                            temp_query_list = sorted_queries[0::cut_lim]
                            num_queries = 9999
                            num_instances = num_instances + 1
                            increase = True
                        else:
                            increase = False
                        delim_list.append(start_queries)
                        query_timing.append(micro_list[temp_index -1])
                        ind_queries.append(temp_index)
                    else:
                        delim_list.append(start_queries)
                        query_timing.append(micro_list[temp_index-1])
                        ind_queries.append(temp_index)
                        increase = False

            cum_query_timing = np.cumsum(query_timing)
           # print 'num instances \t\t- \t%d' %num_instances
           # print 'delim list \t\t- \t', delim_list
           # print 'query timing \t\t- \t', query_timing
           # print 'cumulativequery timing \t- \t', cum_query_timing
           # print 'query indeces \t\t- \t', ind_queries

            for temp_idx in xrange(0,num_instances):
                temp_slice_list = sorted_queries[temp_idx::num_instances]
                count = 0
                ind_queries_idx=0
                for ind_idx, ind in enumerate(temp_slice_list):
                    #unprintprint ind_queries[ind_queries_idx], count
                    if ind_queries[ind_queries_idx] > count:
                        count = count + 1
                    else:
                        count = 0
                        ind_queries_idx = ind_queries_idx + 1
                    #print ind.userid, ind.queryid, ind_queries[ind_queries_idx]
                    ind.batchsize = ind_queries[ind_queries_idx]
                    ind.elapsed_time = cum_query_timing[ind_queries_idx]
                    ind.forward_time = ind.slack_value - cum_query_timing[ind_queries_idx]
                #print '^^^^^^^'
                #for jus_print in temp_slice_list:
                #    print jus_print.userid, jus_print.queryid, \
                #            jus_print.elapsed_time, jus_print.slack_value, \
                #            jus_print.forward_time

                #print 'xxxxxxx'

    #print '_______________________________________________________'

user1err = defaultdict(list )
user1stack = defaultdict(list )
user1slack = defaultdict(list )
user2err = defaultdict(list )
user2slack = defaultdict(list )
user2stack = defaultdict(list )
for service_thrice in list_microservice:
    #print service_thrice.name
    for que_now in service_thrice.queries:
        if que_now.userid == 'user1':
            #print que_now.userid,que_now.queryid, que_now.elapsed_time, \
            #       service_thrice.microservice_dict[que_now.batchsize][service_thrice.input_size]
            user1err[que_now.queryid].append(service_thrice.microservice_dict[que_now.batchsize][service_thrice.input_size])
            user1err[que_now.queryid].append(que_now.elapsed_time - service_thrice.microservice_dict[que_now.batchsize][service_thrice.input_size])
            user1slack[que_now.queryid].append(que_now.slack_value)
        elif que_now.userid == 'user2':
            #print que_now.userid,que_now.queryid, que_now.elapsed_time, \
            #       service_thrice.microservice_dict[que_now.batchsize][service_thrice.input_size]
            user2err[que_now.queryid].append(service_thrice.microservice_dict[que_now.batchsize][service_thrice.input_size])
            #user2err[que_now.queryid].append(que_now.elapsed_time)
            user2err[que_now.queryid].append(que_now.elapsed_time - service_thrice.microservice_dict[que_now.batchsize][service_thrice.input_size])
            user2slack[que_now.queryid].append(que_now.slack_value)

user1 = []
rem_dup1 = []
list_id1 = []
for idx,item in enumerate(user1err):
    temp_list = list(user1err[item])
    list_id1.append(temp_list)
list_id1.sort()
user1 = list(list_id1 for list_id1,_ in itertools.groupby(list_id1))
#for item in user1:
#    print item
#print '------------'



user2 = []
rem_dup2 = []
list_id2 = []
for idx,item in enumerate(user2err):
    temp_list = list(user1err[item])
    list_id2.append(temp_list)


list_id2.sort()
user2 = list(list_id2 for list_id2,_ in itertools.groupby(list_id2))
#for item in user2:
#    print item
print '------------'

user1t = [[j[i] for j in user1] for i in range(len(user1))]
user2t = [[j[i] for j in user2] for i in range(len(user2))]
for item in user1t:
    print item
print '------------'
for item in user2t:
    print item
#raw_data = defaultdict(list )
#for idx in xrange(0, len(user1)):
#    raw_data[idx] = user1t[idx]

#print user1t[0],user2t[0]
#print user1t[1],user2t[1]
#print user1t[2],user2t[2]
#print user1t[3],user2t[3]

### wait #df = pd.DataFrame(raw_data, columns = [np.arange(len(user1t[0]))])
#p1 = plt.bar(np.arange(len(user1t[0])),  user1t[0], color='r')
#p2 = plt.bar(np.arange(len(user1t[1])),  user1t[1], bottom=user1t[0], color='y')
#p3 = plt.bar(np.arange(len(user1t[2])),  user1t[2], bottom= list(map(sum, zip(user1t[0], user1t[1]))), color='b')
#p4 = plt.bar(np.arange(len(user1t[3])),  user1t[3], bottom=list(map(sum, zip(user1t[0], user1t[1], user1t[2]))),  color='g')
##p5 = plt.bar(np.arange(len(user1t[4])),  user1t[4],bottom=user1t[3],  color='y')
##p6 = plt.bar(np.arange(len(user1t[5])),  user1t[5],bottom=user1t[4],  color='b')
#plt.ylim(0,300)
#plt.ylabel('Scores')
#plt.title('Scores by group and gender')
#plt.savefig('done.png')


#print raw_data


