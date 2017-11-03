import microservices as usobj
import helpers as hpobj
import users as userobj
import queries as queobj

######### User INIT ###############
num_user = 2                                        # number of users
list_users = []                                     # list of users

user1           = userobj.UserInfo(1300, 100,'EEFFCC','user1')
list_users.append(user1)

user2       = userobj.UserInfo(1800, 100,'PPBBCCQQ', 'user2')
list_users.append(user2)

#user3       = userobj.UserInfo(900, 100,'XXQQ', 'user3')
#list_users.append(user3)
#hpobj.print_us_info(us.list_microservice)

microservice_ordering = 'PPBBEEFFCCQQ'

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


## ## Old state space calculation
##  # Iterate through state spaces
## #input_size = 2
## max_batch_size = 16
## #print len(list_state_space)
## #print CC.microservice_dict[128][5]
## #sys.exit(0)
## for idx_service, service in enumerate(microservice_ordering):
##     #print service
##     for service_twice in list_microservice:
##         if service_twice.name == service:
##             #print service, service_twice.name, service_twice.input_size, QQ.microservice_dict[1][service_twice.input_size]
##             for que in service_twice.queries:
##                 #temp_dag_single = service + que.dag.split(service)[1]
##                 prev_forward_time = 0
##                 single_time = 0
##                 curr_single_time = 0
##
##                 for service_thrice in list_microservice:
##                     if service_thrice.name in que.dag:
##                         que.single_time = que.single_time + \
##                         service_thrice.microservice_dict[1][service_thrice.input_size]
##                         #print service_thrice.microservice_dict[1] \
##                         #        [service_thrice.input_size], service_thrice.name, service_thrice.input_size
##                     if service_thrice.name == service_twice.name:
##                         curr_single_time = service_thrice.microservice_dict[1][service_thrice.input_size]
##
##
##                 if que.dag.split(service_twice.name)[0] == '':
##                     prev_stage_elapsed = None
##                 else:
##                     #delim_elapsed = len(que.dag.split(service_twice.name)[0])
##                     #print 'coming here'
##                     #print que.dag.split(service_twice.name)[0], delim_elapsed
##                     prev_stage_elapsed = que.dag.split(service_twice.name)[0][-2:]
##
##                 #print prev_stage_elapsed
##                 if prev_stage_elapsed != None:
##                     for service_five in list_microservice:
##                         if service_five.name in prev_stage_elapsed:
##                             for que3 in service_five.queries:
##                                 if que3.userid == que.userid and que3.queryid == que.queryid:
##                                     prev_forward_time = que3.forward_time
##                 else:
##                     prev_forward_time = 0
##                 #print prev_forward_time
##                 #print service_thrice.input_size, curr_single_time, service_thrice.microservice_dict[1][service_thrice.input_size], prev_forward_time
##                 expected_time = ((float(curr_single_time)/que.single_time) * que.sla) + prev_forward_time
##                 #print que.userid, que.queryid, que.single_time, \
##                 #        curr_single_time, expected_time, service_twice.bmax, \
##                 #        prev_forward_time
##                 que.slack_value = expected_time
##             sorted_queries = sorted(service_twice.queries, key=lambda que: que.slack_value )
##
##             #print len(sorted_queries)
##             micro_list = []
##             for item in xrange(1,service_twice.bmax+1):
##                 micro_list.append(service_twice.microservice_dict[item][service_twice.input_size])
##             #print micro_list
##
##             #index = bisect.bisect(micro_list, que.slack_value)
##             #if len(service_twice.queries) < index:
##             #    index = len(service_twice.queries)
##             #else:
##             #    num_queries = index
##             #    cumilative_latency = service_twice.microservice_dict[index][service_twice.input_size]
##             #new_index = index
##             #print '*********Starting trouble**********'
##
##             temp_query_list = sorted_queries
##             num_instances = 1
##             cut_lim = 1
##             increase = True
##             while increase == True:
##                 delim_list = []
##                 query_timing = []
##                 ind_queries = []
##                 max_queries = len(temp_query_list)
##                 cut_lim = cut_lim + 1
##                 #for jus_print in temp_query_list:
##                 #    print jus_print.userid, jus_print.queryid
##                 #print 'watch out for here'
##                 #print max_queries
##                 num_queries = 0
##                 start_queries=0
##                 cumilative_slack = 0
##                 split_slack = temp_query_list[0].slack_value
##                 #print sort_new_que.userid, sort_new_que.queryid
##                 while (num_queries < len(temp_query_list)):
##                     # Bisecting the sorted query list with lowest slack
##                     temp_index = bisect.bisect(micro_list, split_slack)
##                     #print '3*'
##                     #print start_queries, temp_index, split_slack, micro_list[temp_index-1]
##                     if ( temp_index >= max_queries ):
##                         temp_index = max_queries
##                     num_queries = num_queries + temp_index
##                     max_queries = max_queries - temp_index
##                     start_queries = start_queries + temp_index
##
##                     if start_queries < len(temp_query_list):
##                         #account for queuing - cumulative slack is the slack for queuing
##                         cumilative_slack = cumilative_slack + micro_list[temp_index-1]
##                         split_slack = sorted_queries[start_queries].slack_value -\
##                                 cumilative_slack
##                         if split_slack <= micro_list[0]:
##                             temp_query_list = sorted_queries[0::cut_lim]
##                             num_queries = 9999
##                             num_instances = num_instances + 1
##                             increase = True
##                         else:
##                             increase = False
##                         delim_list.append(start_queries)
##                         query_timing.append(micro_list[temp_index -1])
##                         ind_queries.append(temp_index)
##                     else:
##                         delim_list.append(start_queries)
##                         query_timing.append(micro_list[temp_index-1])
##                         ind_queries.append(temp_index)
##                         increase = False
##
##             cum_query_timing = np.cumsum(query_timing)
##            # print 'num instances \t\t- \t%d' %num_instances
##            # print 'delim list \t\t- \t', delim_list
##            # print 'query timing \t\t- \t', query_timing
##            # print 'cumulativequery timing \t- \t', cum_query_timing
##            # print 'query indeces \t\t- \t', ind_queries
##
##             for temp_idx in xrange(0,num_instances):
##                 temp_slice_list = sorted_queries[temp_idx::num_instances]
##                 count = 0
##                 ind_queries_idx=0
##                 for ind_idx, ind in enumerate(temp_slice_list):
##                     #unprintprint ind_queries[ind_queries_idx], count
##                     if ind_queries[ind_queries_idx] > count:
##                         count = count + 1
##                     else:
##                         count = 0
##                         ind_queries_idx = ind_queries_idx + 1
##                     #print ind.userid, ind.queryid, ind_queries[ind_queries_idx]
##                     ind.batchsize = ind_queries[ind_queries_idx]
##                     ind.elapsed_time = cum_query_timing[ind_queries_idx]
##                     ind.forward_time = ind.slack_value - cum_query_timing[ind_queries_idx]
##                 #print '^^^^^^^'
##                 #for jus_print in temp_slice_list:
##                 #    print jus_print.userid, jus_print.queryid, \
##                 #            jus_print.elapsed_time, jus_print.slack_value, \
##                 #            jus_print.forward_time
##
##                 #print 'xxxxxxx'
##
##     #print '_______________________________________________________'

