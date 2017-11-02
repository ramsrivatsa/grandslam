import microservices as us

for idx,item in enumerate(us.list_microservice):
    #for idx,item in enumerate(list_microservice):
    #    print item.name, item.bmax, item.iprange, item.num_queries, item.input_size
    #    if idx == 8:
    #        print item.name, item.bmax, item.iprange, item.num_queries, item.input_size
    #        print(json.dumps(item.microservice_dict, indent = 4))
    #        print(json.dumps(item.microservice_data_dict, indent = 4))
    print item.name, item.bmax, item.iprange, item.num_queries, item.input_size
