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
    cumilative_time         = 0
    que_time                = 0
    compute_time            = 0

