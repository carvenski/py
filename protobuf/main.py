from test_pb import VMInfoConfig

# use VMInfoConfig class here, which is generated from pb file.
pb_obj = VMInfoConfig()
pb_obj.Memory = 1
pb_obj.Cpu = 2
pb_str = pb_obj.SerializeToString()
print("pb obj => str => bytes")
print(pb_str)
print([i.encode("utf8") for i in pb_str])

pb_obj2 = VMInfoConfig()
pb_obj2.ParseFromString(pb_str)
print("str => pb obj")
print(pb_obj2)


