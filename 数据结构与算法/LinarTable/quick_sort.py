"""
quick sort

     |    |     |   | 
-------------------------------
| | | | | | | | | | | | | | | |
-------------------------------
i    i    i     j   j         j
->   |    |     |   |        <-

"""
def quick_sort(list, l, r):	
	if l > r:
		return
	i, j = l, r
	pivot = list[l]
	while i < j:  #### need i < j everywhere !!!!
		# scan from right
		while i < j and pivot <= list[j]:
			j -= 1
		if i < j:
			list[i] = list[j]
			i += 1
		# scan from left
		while i < j and list[i] <= pivot:
			i += 1
		if i < j:
			list[j] = list[i]
			j -= 1
	# found i
	list[i] = pivot
	quick_sort(list, l, i-1)
	quick_sort(list, i+1, r)


l = [32,435,5,6,657,562,443,65,6,0,5665,6,562,45,5666,65,34,665,698,45,9]
print(l)
quick_sort(l, 0, len(l)-1)
print(l)



