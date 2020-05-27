from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor(10)

args = [
        (queryAllDCHandler, kw, 'compute/datacenter/sync'),
        (queryAllClusterHandler, kw, 'compute/cluster/sync'),
        (queryAllPortgroupHandler, kw, 'compute/portgroup/sync'),
        (queryAllImageHandler, kw, 'compute/image/sync'),
        (queryAllDatastoreHandler, kw, 'compute/datastore/sync'),
        (queryAllVMSnapshotHandler, kw, 'compute/snapshot/sync'),
        (queryAllPhysicalhostHandler, kw, 'compute/physicalhost/sync'),
        (queryAllVMDiskHandler, kw, 'compute/disk/sync'),
        (queryAllVMHandler, kw, 'compute/host/sync')
]
result_list = pool.map(_queryAllResourceHandler, args)

for i in result_list:
    print(i)
    
# ThreadPoolExecutor的map函数的使用： map返回的结果是有序结果；是根据迭代函数执行顺序返回的结果.
#   也就是说，result_list里面的结果出来的顺序是和args参数里面进去的顺序保持一致的 !!


