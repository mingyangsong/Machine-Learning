#!/usr/bin/env python

import sys
import math

#-------------------------
#   test naive Bayes
#-------------------------
def test_NB(train_dic, test_set):
    result={}

    (p_con, p_lib, con_dic, lib_dic)=train_dic

    for item in test_set:
	test_list=open("data/"+item).read()[:-1].lower().split("\n")
	res_con=0.0
        res_lib=0.0
	
	for word in test_list:
	    res_con=res_con+(float)(con_dic.get(word,"0"))
	    res_lib=res_lib+(float)(lib_dic.get(word,"0"))

	res_con=res_con+p_con
        res_lib=res_lib+p_lib

	if res_con < res_lib:
	    print item+" C"
	else:
	    print item+" L"

#-------------------------
#   train naive Bayes
#-------------------------
def train_NB(train_set, test_set, F):
    con_str=""
    lib_str=""
    tot_str=""
    for con in train_set[0]:
	con_str=con_str+open("data/"+con).read()[:-1]
    for lib in train_set[2]:
	lib_str=lib_str+open("data/"+lib).read()[:-1]
   
    for i in range(0,64):
	tot_str=tot_str+open("data/con"+str(i)+".txt").read()[:-1]

    for i in range(0,56):
	tot_str=tot_str+open("data/lib"+str(i)+".txt").read()[:-1]


    con1_list=con_str.lower().split("\n")
    lib1_list=lib_str.lower().split("\n")
    tot_list=tot_str.lower().split("\n")

    word_freq={}
    for word in tot_list:
        word_freq[word] = word_freq.get(word,0) + 1

    i=0
    rem_list={}
    for w in sorted(word_freq, key=word_freq.get, reverse=True):
	i=i+1 
 	rem_list[w]=0
        if i == 50:
	    break

    for w in word_freq:
        if word_freq.get(w) < int(F):
	    rem_list[w]=0

    con_num=train_set[1]
    lib_num=train_set[3]

    p_con=-math.log((float)(con_num)/(con_num+lib_num))
    p_lib=-math.log((float)(lib_num)/(con_num+lib_num))

    con_dic={}
    lib_dic={}
    con_word_freq={}
    lib_word_freq={}

    con_list=[]
    lib_list=[]

    for co in con1_list:
	if co not in rem_list:
	    con_list.append(co)

    for li in lib1_list:
	if li not in rem_list:
	    lib_list.append(li)

    for word in con_list:
        con_word_freq[word] = con_word_freq.get(word,0) + 1  
  
    for word in lib_list:
	lib_word_freq[word] = lib_word_freq.get(word,0) + 1  

    con_list_size=len(con_list)
    lib_list_size=len(lib_list)
    
    vocabulary=set(con_list+lib_list)
    num_voc=len(vocabulary)

    for k,v in con_word_freq.items():
	score=-math.log((float)(v+1)/(con_list_size+num_voc))
	con_dic[k]=score

    for word in vocabulary:
	if con_dic.get(word,"empty")=="empty":
	    con_dic[word]=-math.log((float)(1.0)/(con_list_size+num_voc))

    for k,v in lib_word_freq.items():
	score=-math.log((float)(v+1)/(lib_list_size+num_voc))
	lib_dic[k]=score

    for word in vocabulary:
	if lib_dic.get(word,"empty")=="empty":
	    lib_dic[word]=-math.log((float)(1.0)/(lib_list_size+num_voc))
    
    return [p_con, p_lib, con_dic, lib_dic]

#-------------------------
#   get test list
#-------------------------
def get_test(filestr):
    file_list=open("split/"+filestr).read()[:-1].split("\n")
    return file_list

#-------------------------
#   get train list
#-------------------------
def get_train(filestr):
    file_list=open("split/"+filestr).read()[:-1].split("\n")

    con_num=0
    lib_num=0
    con_list=[]
    lib_list=[]
    for i in file_list:
	if i[:3]=="con":
	    con_num=con_num+1
            con_list.append(i)
	else: 
 	    lib_num=lib_num+1
	    lib_list.append(i)

    return [con_list,con_num,lib_list,lib_num]

#-------------------------
#    main
#-------------------------
def main():
    if len(sys.argv) >= 4:
	train_set=get_train(sys.argv[1])
        test_set=get_test(sys.argv[2])
	train_dic=train_NB(train_set, test_set, sys.argv[3])
     	test_NB(train_dic, test_set)
    else:
    	print "Please add train and test files"

if __name__ == "__main__": main()
