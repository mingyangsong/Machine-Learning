#!/usr/bin/python

import sys

k=int(sys.argv[1])
correct=0
n=0
a=[]
b=[]
for line in sys.stdin:
	n=n+1
	line=line.replace("\n","")
	if n<=k:
		b.append(line)
	a.append(line)
for i in range(k,n):
	sun=0
	rain=0
	for j in range(i-k,i):
		if a[j]=='sun':
			sun=sun+1
		else:
			rain=rain+1
	if sun>rain:
		b.append("sun")
	else:
		b.append("rain")
for i in range(k,n):
	if a[i]==b[i]:
		correct=correct+1
accuracy=float(correct)/float(n-k)
print accuracy
