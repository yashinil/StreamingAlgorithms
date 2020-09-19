#command to run the task
#python second.py users.txt 300 30 second_output.csv
#python second.py users.txt 1 1 second_output.csv

from blackbox import BlackBox
import binascii
import csv
import sys
import time

#timer start
start_time=time.time()

input_file=sys.argv[1]
stream_size=int(sys.argv[2])
num_of_asks=int(sys.argv[3])
output_file=sys.argv[4]

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

fm_list=list()

def myhashs(s):
    #print(s)
    s=int(binascii.hexlify(s.encode('utf8')),16)
    # print(s)
    results=[] 
    for f in hash_functions_list:
        hash_value=( f[0]*s + f[1] ) % 691
        results.append(hash_value)
    return results

def flajolet_martin_algo(data):
    unique_users=set()
    trailing_zeros=[0]*number_of_hashes
    for user in data:
        unique_users.add(user)
        hashes=myhashs(user)
        for i in range(len(hashes)):
            binary_hash=bin(hashes[i])
            # print(binary_hash)
            if(trailing_zeros[i]<len(binary_hash) - len(binary_hash.rstrip('0'))):
                trailing_zeros[i] = len(binary_hash) - len(binary_hash.rstrip('0'))    
                
    #print(trailing_zeros)
    summation=0
    for x in trailing_zeros:
        summation+=pow(2,x)
    avg=summation/number_of_hashes
    #print(avg,len(unique_users))
    fm_list.append((len(unique_users),round(avg)))

bx = BlackBox()

for _ in range(num_of_asks):
    stream_users = bx.ask(input_file, stream_size)
    flajolet_martin_algo(stream_users)

with open(output_file, mode='w', newline='') as fm_file:
    fm_writer = csv.writer(fm_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    fm_writer.writerow(["Time","Ground Truth","Estimation"])
    for i in range(len(fm_list)):
        fm_writer.writerow([i,fm_list[i][0],fm_list[i][1]])

our_solution=0
actual_solution=0
for x in fm_list:
    our_solution+=x[1]
    actual_solution+=x[0]

result=our_solution/actual_solution
print("Results: ",result)

print("Duration: %s" % (time.time() - start_time))