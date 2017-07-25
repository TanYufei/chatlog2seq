# -*- coding: utf-8 -*-
# @Time    : 7/24/17 2:40 PM
# @Author  : tyf_aicyber
# @Site    : 
# @File    : dialogue2seq.py
# @Software: PyCharm

import pandas as pd
import re
import numpy as np

def read_xlxs2(filename=u'../dataset/聊天记录10月.xlsx'):
    df = pd.read_excel(filename)
    chatloglist= df[u'聊天记录'][365]
    print chatloglist

def read_xlxs(filename=u'../dataset/聊天记录11月.xlsx'):
    df = pd.read_excel(filename)
    chatloglist= df[u'聊天记录']
    print len(chatloglist)

    seqlist=[]
    talkerlist=[]
    chatlog_index=[]

    for i,chatlog in enumerate(chatloglist):
        try:
            # print i
            speakpersonlist, sequenceslist=chatlog2seq(chatlog)

            c_index=list(np.ones(len(sequenceslist))*i)
            seqlist.extend(sequenceslist)
            talkerlist.extend(speakpersonlist)
            chatlog_index.extend(c_index)
        except:
            print i
            continue

    columns = ['chatlog_id', 'seq', 'speaker']
    pd.DataFrame(columns=columns, data=list(zip(chatlog_index,seqlist,talkerlist))).to_csv(u'../dataset/聊天记录11月.csv',encoding='utf-8',index=False,sep='\t')

def chatlog2seq(chatlog):
    sentenceslist = chatlog.strip().split('\n')

    speaker=[]
    content=[]
    i=0
    while i<len(sentenceslist)-2:
        # print sentenceslist[i]
        if re.match(u'(^\d{2}:\d{2}$|.+\d\d:\d{2}$|^\d{4}$|^已回复\d{4}$)',sentenceslist[i]):
            # print sentenceslist[i]
            speaker.append(sentenceslist[i+1])
            content.append(sentenceslist[i+2])
            i+=3
        else:
            i+=1
    content.reverse()
    speaker.reverse()
    assert content !=[]

    # for cou,sp in zip(content,speaker):
    #     print sp
    #     print cou
    return seqReduce(content,speaker)

def seqReduce(content,speaker):
    assert len(content) == len(speaker)

    sequenceslist=[]
    speakperson=[]
    num=0
    sequenceslist.append(content[0])
    speakperson.append(speaker[0])
    for i in range(1,len(content)):
        if speaker[i]==speaker[i-1]:
            sequenceslist[num]=sequenceslist[num]+'\t'+content[i]
        else:
            sequenceslist.append(content[i])
            speakperson.append(speaker[i])
            num+=1
    assert len(speakperson)==len(sequenceslist)
    # for sp,sequences in zip(speakperson,sequenceslist):
    #     print sp
    #     print sequences
    return speakperson,sequenceslist


if __name__=='__main__':
    read_xlxs()
    # read_xlxs2()