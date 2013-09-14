#!/usr/bin/env python

import sys
import math

#-------------------------
#   test naive Bayes
#-------------------------
def test_NB(train_dic, test_set):
    result={}

    (p_con, p_lib, con_dic, lib_dic)=train_dic

    #print p_con,p_lib
    for item in test_set:
	test_list=open("data/"+item).read()[:-1].lower().split("\n")
	res_con=0.0
        res_lib=0.0
	
	for word in test_list:
	    res_con=res_con+(float)(con_dic.get(word,"0"))
	    res_lib=res_lib+(float)(lib_dic.get(word,"0"))
	    #print res_con
	#print res_con,res_lib
	res_con=res_con+p_con
        res_lib=res_lib+p_lib
        #print res_con,res_lib
	if res_con < res_lib:
	    result[item]="C"
	    print item+" C"
	else:
	    result[item]="L"
	    print item+" L"
    return result    

#-------------------------
#   train naive Bayes
#-------------------------
def train_NB(train_set):
    con_str=""
    lib_str=""
    for con in train_set[0]:
	con_str=con_str+open("data/"+con).read()[:-1]
    for lib in train_set[2]:
	lib_str=lib_str+open("data/"+lib).read()[:-1]
    con_list=con_str.lower().split("\n")
    lib_list=lib_str.lower().split("\n")
    #print lib_list

    vocabulary=set(con_list+lib_list)
    num_voc=len(vocabulary)
    #print num_voc
    
    con_num=train_set[1]
    con_list_size=len(con_list) 
    lib_num=train_set[3]
    lib_list_size=len(lib_list)

    #print con_list_size
    #print lib_list_size

    p_con=-math.log((float)(con_num)/(con_num+lib_num))
    p_lib=-math.log((float)(lib_num)/(con_num+lib_num))

    con_dic={}
    lib_dic={}
    con_word_freq={}
    lib_word_freq={}

    for word in con_list:
        con_word_freq[word] = con_word_freq.get(word,0) + 1  
  
    for k,v in con_word_freq.items():
	score=-math.log((float)(v+1)/(con_list_size+num_voc))
	con_dic[k]=score

    for word in vocabulary:
	if con_dic.get(word,"empty")=="empty":
	    con_dic[word]=-math.log((float)(1.0)/(con_list_size+num_voc))

    for word in lib_list:
        lib_word_freq[word] = lib_word_freq.get(word,0) + 1  
  
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
    if len(sys.argv) >= 3:
	train_set=get_train(sys.argv[1])
        test_set=get_test(sys.argv[2])
	train_dic=train_NB(train_set)
     	result=test_NB(train_dic, test_set)
	#for k,v in result.items():
	 #   print k,v
    else:
    	print "Please add train and test files"

if __name__ == "__main__": main()
