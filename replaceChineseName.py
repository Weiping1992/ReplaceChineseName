#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-06-26 15:27:24
# @Author  : weiping (chengwei2011ww@163.com)
# @Link    : https://github.com/Weiping1992
# @Version : 0.15

# python version 2.7

'''
说明：
    实现将指定路径中的中文名称的文件和文件夹改成指定名称
    需要提前配置好翻译的配置文件Ch2En.json（放在脚本的同一目录下）,配置见样例
使用方法：
    python replaceChineseName.py --no-recurse --path=/opt/replaceChineseName_test --config=./Ch2En.json
'''

import os
import re
import json
import getopt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def check_chinese_characters(str):
    for ch in str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

#windows filename encode with gbk
def rename_Chinese(path,recursive=1):
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
            if recursive=1:
                rename_Chinese(path_sub)
        for file in files:
            file_uni=os.path.join(file).decode('gbk')
            #print repr(file_uni)
            if check_chinese_characters(file_uni):
                name_new=dicTranslate[file_uni]
                #print name_new
                os.rename(os.path.join(root,file),os.path.join(root.name_new))

def find_Chinese(path):
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
    TargetPath=str(os.getcwd())
    TranslateConfig='Ch2En.json'
    recurse=1        #默认是递归的
    try:
        ops,args=getopt.getopt(sys.argc[1:],'h',['help','no-recurse','path=','config='])
    except:
        sys.exit(1)
    for op,value in ops:
        if op in ('-h','--help'):
            usage()
            sys.exit(0)
        if op in ('--no-recurse'):
            recurse=0
        if op in ('--path'):
            TargetPath=value
        if op in ('--config'):
            TranslateConfig=value

    dicTranslate=json.load(open(TranslateConfig,'r'))
    #print dicTranslate

    find_Chinese(TargetPath)
    while(1):
        try:
            rename_Chinese(TargetPath,recurse)
        except UnicodeDecodeError:
            continue
        else:
            break
    find_Chinese(TargetPath)
