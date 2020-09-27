#!/usr/bin/python

import sys
import numpy as np

mbps = []

filename = sys.argv[1]
runNum = sys.argv[3]

data = np.loadtxt(filename, dtype=np.str, delimiter=",")
latency = data[:,0].astype(np.float)
cnt     = data[:,1].astype(np.int)

length = len(latency);

for index in range(length):
    for icnt in range(0,cnt[index]):
        mbps.append(latency[index])





#f = open(filename, "r")
#flag = False
#for line in f:
#	if line.startswith("[main]"):
#	    flag = True
#            continue
#        if line.startswith("event"):
#            break
#        if line.startswith("PMdropping"):
#            continue
#        if line.startswith("random"):
#            continue
#        if line.startswith("[clustering_classification_PM_random_shedding]"):
#            continue
#        if flag:
#	    x = float(line)/1000
#	    mbps.append(x)

print("{0: >15} {1: 10.2f} {2: 10.2f} {3: 10.2f} {4: 10.2f} {5: 10.2f} {6: 10.2f} {7: 10.2f} {8: 10.2f} {9: >10} {10: 10.2f} ".format( sys.argv[2], np.min(mbps), np.mean(mbps), np.max(mbps), np.percentile(mbps, 5), np.percentile(mbps, 25), np.percentile(mbps, 50), np.percentile(mbps, 75), np.percentile(mbps, 95), runNum, np.std(mbps)))

sys.exit(0)
