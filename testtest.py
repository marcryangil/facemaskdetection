lst=[["a", "b", "c"], ["dad", "e", "f"], ["g","h"]]
check="ad"

rows_to_be_hidden = ["{}".format(index1) for index1,value1 in enumerate(lst) for index2,value2 in enumerate(value1) if check not in value2]

#print(rows_to_be_hidden)

print(bool(1))