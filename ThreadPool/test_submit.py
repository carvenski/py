from concurrent import futures

pool = futures.ThreadPoolExecutor(10)

args = [(queryAllDCHandler, kw, 'compute/datacenter/sync'),
        (queryAllClusterHandler, kw, 'compute/cluster/sync'),                        
        (queryAllPortgroupHandler, kw, 'compute/portgroup/sync'),
        (queryAllImageHandler, kw, 'compute/image/sync'),
        (queryAllDatastoreHandler, kw, 'compute/datastore/sync'),
        (queryAllVMSnapshotHandler, kw, 'compute/snapshot/sync'),
        (queryAllPhysicalhostHandler, kw, 'compute/physicalhost/sync'),
        (queryAllVMDiskHandler, kw, 'compute/disk/sync'),
        (queryAllVMHandler, kw, 'compute/host/sync'),]

result_list = []

for arg in args:
	#这里使用submit来提交任务到线程池,而不是直接使用map
	future = pool.submit(_queryAllResourceHandler, arg)
    result_list.append(future)

# 这里使用futures.as_completed来等待每个future完成以及它的结果,
# 注意这里的返回无序的,哪个future先完成了,哪个就先走掉！
for f in futures.as_completed(result_list):
	# future会按照完成的先后来返回
    print( f.done(), f.result() )

    
    
