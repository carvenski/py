# use hash to group data
N = 10
for x in xrange(1,100):
	s = "%d-data-%d-%d" % (x,x,x)
	h = hash(s)
  # hash值有负数,但负数也可取模的
	print("data: %s, hash: %d, catagory: %d " % (s, h, h%N))



