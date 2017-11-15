from collections import defaultdict
import microservices as usobj
import helpers as hpobj
import users as userobj
import queries as queobj
import bisect

######### User INIT ###############
num_user = 4                                        # number of users
list_users = []                                     # list of users

##user1           = userobj.UserInfo(800, 10,'PPBBCC','user1')
##list_users.append(user1)
##
##user2       = userobj.UserInfo(600, 5,'EEFF', 'user2')
##list_users.append(user2)
##
##user3       = userobj.UserInfo(1500, 7,'DDBBCC', 'user3')
##list_users.append(user3)
##
##user4       = userobj.UserInfo(600, 13,'GGDDEEFF', 'user4')
##list_users.append(user4)


user1           = userobj.UserInfo(2500, 43,'PPBBCC','user1')
list_users.append(user1)

user2       = userobj.UserInfo(1200, 60,'EEFF', 'user2')
list_users.append(user2)

user3       = userobj.UserInfo(1900, 35,'DDBBCC', 'user3')
list_users.append(user3)

user4       = userobj.UserInfo(1300, 60,'GGDDEEFF', 'user4')
list_users.append(user4)

#user3       = userobj.UserInfo(100, 15,'AACCGG', 'user3')
#list_users.append(user3)
#hpobj.print_us_info(us.list_microservice)

#microservice_ordering = 'PPBBEEFFCCQQ'
#microservice_ordering = ['PP', 'BB', 'EE', 'FF', 'AA' , 'CC', 'QQ', 'GG']
#microservice_ordering = ['AA', 'EE', 'PP']
microservice_ordering = ['PP', 'DD', 'BB', 'CC', 'EE' , 'FF']

######### Microservice INIT ###############

'''
This piece of code updates the following.
1. number of queries for each microservice considering all users.
2. Initializing list of queries for each microservice consisring all users.
'''
for service in usobj.list_microservice:
    temp_queries = []
    for usr in list_users:
        if service.name in usr.dag:
            ## updating the number of queries ##
            service.num_queries = service.num_queries + usr.freq
            for que in xrange(0,usr.freq):
                #print service.name
                #print que+1
                q = queobj.Query(usr.userid, 999, 999, que+1, usr.dag, usr.sla)
                temp_queries.append(q)
                del q
    service.queries = temp_queries
    del temp_queries
#    #print '-------------'

#print microservice_ordering
#for temp_var in list_users:
#    print temp_var.userid, temp_var.dag
#print user1.dag, user2.dag, user3.dag
for idx_service, service in enumerate(microservice_ordering):
    #print '----------------------------------------------'
    #print service
    for service_twice in usobj.list_microservice:
        #print service_twice.name
        if service_twice.name == service:
            #print service_twice.name, service_twice.alias, \
            #        service_twice.iprange[len(service_twice.iprange)-1]
            #print service, service_twice.name, service_twice.input_size, \
            #        service_twice.num_queries, service_twice.num_instances
            for que in service_twice.queries:
                #temp_dag_single = service + que.dag.split(service)[1]
                prev_forward_time = 0
                single_time = 0
                curr_single_time = 0

                if que.dag.split(service_twice.name)[0] == '':
                     prev_stage_elapsed = None
                else:
                    #delim_elapsed = len(que.dag.split(service_twice.name)[0])
                    #print 'coming here'
                    #print que.dag.split(service_twice.name)[0], delim_elapsed
                    prev_stage_elapsed = que.dag.split(service_twice.name)[0]
                #print prev_stage_elapsed

                 #print prev_stage_elapsed
                prev_elapsed_time = 0
                if prev_stage_elapsed != None:
                    for service_five in usobj.list_microservice:
                        if service_five.name in prev_stage_elapsed:
                            #print service_five.name
                            for que3 in service_five.queries:
                                if que3.userid == que.userid and que3.queryid == que.queryid:
                                    #print que3.elapsed_time
                                    prev_elapsed_time = prev_elapsed_time + que3.elapsed_time
                else:
                    prev_elapsed_time = 0
                que.slack_value = que.sla - prev_elapsed_time
                #print que.userid, que.queryid, que.sla, que.slack_value,  prev_elapsed_time

            sorted_queries = sorted(service_twice.queries, key=lambda que: que.slack_value )
            #for item in sorted_queries:
            #    print item.userid, item.queryid

            temp_query_list = sorted_queries
            num_instances = service_twice.num_instances
            cut_lim = 1


            for temp_idx in xrange(0,num_instances):
                temp_slice_list = temp_query_list[temp_idx::num_instances]
                #print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                #print num_instances
                #print service_twice.name, service_twice.iprange[len(service_twice.iprange)-1]
                # change this to a while loop and call it off!
                #for item in temp_slice_list:
                total_elapsed_time = 0
                queuing_time       = 0
                while temp_slice_list:
                    #print '*********'
                    #implement all the functions here
                    getbatch_dict = defaultdict(lambda  : defaultdict(float))
                    getbatch_list = []
                    for key,value in service_twice.microservice_dict.iteritems():
                        getbatch_dict[key] = service_twice.microservice_dict[key]\
                                [service_twice.iprange[len(service_twice.iprange)-1]]
                        getbatch_list.append(service_twice.microservice_dict[key][service_twice.input_size])
                    curr_slack_value = temp_slice_list[0].slack_value - total_elapsed_time
                    index = bisect.bisect(getbatch_list, curr_slack_value)
                    if index == 0:
                        index = 1
                    #print index, len(getbatch_list), getbatch_list[index-1],\
                    #        len(temp_slice_list), temp_slice_list[0].slack_value


                    if index > len(temp_slice_list):
                        index = len(temp_slice_list)
                    #print index, len(getbatch_list), temp_slice_list[0].\
                    #        slack_value, curr_slack_value, getbatch_list[index-1]

                    #for item in temp_slice_list[0:index]:
                    #    print item.userid, item.queryid, item.sla, index

                    ##assigning values for the forward run
                    total_elapsed_time = total_elapsed_time + getbatch_list[index-1]
                    for item in temp_slice_list[0:index]:

                        if item.dag.split(service_twice.name)[0] == '':
                             prev_stages = None
                        else:
                            #delim_elapsed = len(que.dag.split(service_twice.name)[0])
                            #print 'coming here'
                            #print que.dag.split(service_twice.name)[0], delim_elapsed
                            prev_stages = item.dag.split(service_twice.name)[0]
                        #print prev_stages

                        #print prev_stage_elapsed
                        temp_cumilative_time = 0
                        if prev_stages != None:
                            for service_seven in usobj.list_microservice:
                                if service_seven.name in prev_stages:
                                    #print service_five.name
                                    for que4 in service_seven.queries:
                                        if que4.userid == item.userid and que4.queryid == item.queryid:
                                            #print que3.elapsed_time
                                            #prev_forward_time = que3.forward_time
                                            temp_cumilative_time = temp_cumilative_time +\
                                                    que4.elapsed_time
                        else:
                            temp_cumilative_time = 0

                        item.batch_size = index
                        item.elapsed_time = total_elapsed_time
                        item.cumilative_time = total_elapsed_time +  temp_cumilative_time
                        item.que_time = queuing_time
                        item.compute_time = getbatch_list[index-1]

                        #print item.userid, item.queryid, item.sla, index,\
                        #        item.elapsed_time, getbatch_list[index-1],\
                        #        total_elapsed_time

                    queuing_time = queuing_time + getbatch_list[index-1]
                    del temp_slice_list[0:index]



                    #if getbatch_list[index-1] > temp_slice_list[0].slack_value:
                    #    del temp_slice_list[:]
                    #if index >= len(temp_slice_list):
                    #    ## batch everything completely
                    #    del temp_slice_list[:]
                    #else:
                    #    del temp_slice_list[0:index-1]
                    #print item.userid, item.queryid, item.sla, index, getbatch_list[index-1]

                        #print key,service_twice.microservice_dict[key][128]
                    #print temp_dict
                    #target = 93.49
                    #key2, value2 = min(dict.items(), key=lambda (_, v): abs(v - target))
                    #print key2,value2
                    #print microservice_dict[key2][value2]

for idx_service, service in enumerate(microservice_ordering):
    print '----------------------------------------------'
    print service
    for service_twice in usobj.list_microservice:
        #print service_twice.name
        if service_twice.name == service:
            #print service_twice.name
            for que in service_twice.queries:
                #print que.userid, que.queryid, que.sla, que.batch_size,\
                #        que.slack_value,  que.elapsed_time, que.cumilative_time
                #print que.userid, que.queryid, que.sla, que.compute_time, \
                #        que.que_time, que.elapsed_time, \
                #        que.cumilative_time
                print service, que.userid, que.queryid, que.sla, \
                        que.compute_time, que.que_time, que.elapsed_time, \
                        que.cumilative_time
