#command to run the task
#python first.py users.txt 100 30 first_output.csv

#FPR = FP / (FP + TN). 

from blackbox import BlackBox
import binascii
import csv
import sys
import time

#timer start
start_time=time.time()

n=69997
input_file=sys.argv[1]
stream_size=int(sys.argv[2])
num_of_asks=int(sys.argv[3])
output_file=sys.argv[4]

previous_users=set()

global_filter=[0]*n

hash_functions_list=list()
prime_numbers=[73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 
127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 
179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 
233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 
283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 
353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 
419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 
467, 479, 487, 491, 499, 503, 509, 521, 523, 541,
547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 
607, 613, 617, 619, 631, 641, 643, 647, 653, 659]

number_of_hashes=100

for i in range(number_of_hashes):
    hash_functions_list.append((prime_numbers[i],prime_numbers[len(prime_numbers)-i-1]))
#print(hash_functions_list)

fpr_list=list()

def myhashs(s):
    #print(s)
    s=int(binascii.hexlify(s.encode('utf8')),16)
    # print(s)
    results=[] 
    for f in hash_functions_list:
        hash_value=( f[0]*s + f[1] ) % n
        results.append(hash_value)
    return results

def bloom_filtering(data):
    # print(data)
    number_of_fp=0
    number_of_tn=0
    for user in data:
        hashes=myhashs(user)
        # print(hashes)
        # flag=1 means bloom filter says user is present
        # flag=0 means bloom filter says user is not present 
        flag=1
        for pos in hashes:
            if global_filter[pos]!=1:
                flag=0
                break

        if flag==0:
            #if the user does not exist in the stream
            if user not in previous_users:
                number_of_tn+=1
            #print("user not present")
            previous_users.add(user)
            for pos in hashes:
                global_filter[pos]=1
        # print(global_filter)
        else:
            if user not in previous_users:
                number_of_fp+=1
            #print("present")

        # if flag!=isUserPresent:
            

    fpr=number_of_fp/(number_of_fp+number_of_tn)
    fpr_list.append(fpr)

bx = BlackBox()
# stream_users = bx.ask("users.txt", 100)

for _ in range(num_of_asks):
    stream_users = bx.ask(input_file, stream_size)
    bloom_filtering(stream_users)

# print(fpr_list)

with open(output_file, mode='w', newline='') as fpr_file:
    fpr_writer = csv.writer(fpr_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    fpr_writer.writerow(["Time","FPR"])
    for i in range(len(fpr_list)):
        fpr_writer.writerow([i,fpr_list[i]])

print("Duration: %s" % (time.time() - start_time))