#command to run the task
#python third.py users.txt 100 30 third_output.csv
#python third.py users.txt 1 1 third_output.csv

#csv file should have the appropriate headers

from blackbox import BlackBox
import binascii
import csv
import sys
import time
import random

#timer start
start_time=time.time()

input_file=sys.argv[1]
stream_size=int(sys.argv[2])
num_of_asks=int(sys.argv[3])
output_file=sys.argv[4]

rs_list=list()

reservior=list()
stream_count=0

random.seed(553) 

def reservoir_sampling(data):
    # print(data)
    global stream_count
    for user in data:
        stream_count+=1
        if len(reservior)!=100:
            reservior.append(user)
        else:
            if random.randint(0, 100000) % stream_count < 100:
                # print("1")
                index=random.randint(0,100000) % 100
                # print(index)
                reservior[index]=user
            # else:
                # print("0")
    
        if stream_count%100==0:
            rs_list.append([stream_count,reservior[0],reservior[20],reservior[40],reservior[60],reservior[80]])
    # print(reservior)

bx = BlackBox()

for _ in range(num_of_asks):
    stream_users = bx.ask(input_file, stream_size)
    reservoir_sampling(stream_users)

# print(rs_list)
with open(output_file, mode='w', newline='') as rs_file:
    rs_writer = csv.writer(rs_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    rs_writer.writerow(["seqnum","0_id","20_id","40_id","60_id","80_id"])
    for i in range(len(rs_list)):
        rs_writer.writerow(rs_list[i])

print("Duration: %s" % (time.time() - start_time))