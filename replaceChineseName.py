#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-26 15:27:24
# @Author  : weiping (chengwei2011ww@163.com)
# @Link    : https://github.com/Weiping1992
# @Version : 0.1

import os
import re
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

TargetPath="/opt/replaceChineseName_test"
dicTranslate=json.load(open('Translate.json'))
#print dicTranslate

def check_chinese_characters(str):
    for ch in str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def rename_Chinese(path):
    for root,dirs,files in os.walk(path):
        for dir in dirs:
            dir_uni=os.path.join(dir).encode('gbk')
            #print repr(dir_uni)
            path_sub=os.path.join(root,dir)
            if check_chinese_characters(dir_uni):
                name_new=dicTranslate[dir_uni]
                #print name_new
                #print root
                path_sub=os.path.join(root,name_new)
                os.rename(os.path.join(root,dir),path_sub)
            rename_Chinese(path_sub)
        for file in files:
            file_uni=os.path.join(file).decode('gbk')
            #print repr(file_uni)
            if check_chinese_characters(file_uni):
                name_new=dicTranslate[file_uni]
                #print name_new
                os.rename(os.path.join(root,file),os.path.join(root.name_new))

def check_done(path):
    num_chinese=0
    List_ch=[]
    for root,dirs,files in os.walk(path):
        for dir in dirs:
            dir_uni=os.path.join(dir).decode('gbk')
            if check_chinese_characters(dir_uni):
                List_ch.append(os.path.join(root,dir).decode('gbk').encode('utf-8'))
                num_chinese+=1
        for file in files:
            file_uni=os.path.join(file).decode('gbk')
            if check_chinese_characters(file_uni):
                List_ch.append(os.path.join(root,file).decode('gbk').encode('uft-8'))
                num_chinese+=1
    if num_chinese == 0:
        print "checked! No Chinese left. "
    else:
        print List_ch

if __name__ == '__main__':
    check_done(TargetPath)
    run=1
    while(run):
        try:
            rename_Chinese(TargetPath)
        except UnicodeDecodeError:
            run=1
        else:
            run=0

    check_done(TargetPath)
