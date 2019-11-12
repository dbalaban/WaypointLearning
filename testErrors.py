import numpy as np
import subprocess
import time
import os

f = open("error.txt", "r")

f1 = f.readlines()
count_calls = 0
count_errors = 0
for x in f1:
    count_calls += 1
    if os.path.exists('test.txt'):
      os.remove('test.txt')
    y = ('test.txt '+ x).split()
    process = subprocess.call(['bin/eval'] + y)
    if process > 0:
        count_errors += 1
        
print(str(count_errors)+" errors out of "+str(count_calls) + " calls.")
    