from src.bucketList import *

b = BucketList("Countries To Visit")
b.add_item("Bulgaria")
b.add_item("China")
b.add_item("Iceland")

for i in b.items:
    print(i.title)