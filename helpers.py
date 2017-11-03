import json

def print_us_info(us_list):
    for idx,item in enumerate(us_list):
        print item.name, item.bmax, item.iprange, item.num_queries, item.input_size, item.input_size
        #if idx == 8:
        #    print item.name, item.bmax, item.iprange, item.num_queries, item.input_size
        #    print(json.dumps(item.microservice_dict, indent = 4))
        #    print(json.dumps(item.microservice_data_dict, indent = 4))


