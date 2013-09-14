#!/usr/bin/python

import sys

n=0
a=[]
for line in sys.stdin:
	n=n+1
	lines=line.split(' ');
	lines[0]=float(lines[0])
	a.append(lines)
a.sort()
for i in a:
	print i
