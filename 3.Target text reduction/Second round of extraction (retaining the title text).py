#  -*-coding:utf8 -*-

"""
Created on 2021 8 25

@author: 陈雨
"""

import re


'''二轮提取(保留有职称的文本、未去重)'''
# 逐行判断当前文本是否包含职称
# 职称大致的分为13类

# 股东
name_list1 = ["股东","控股股东","关联股东","非关联股东","新股东","老股东","大股东","中股东","小股东","中小股东"]
f1 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\shareholder.txt","w+", encoding="utf-8")  
# 董事会
name_list2 = ["董事长","副董事长","董事会秘书","董事长秘书","董秘","董事候选人","执行董事","独立董事","独立董事候选人","非独立董事","非独立董事候选人","非独立董事会候选人","独立董事委员","实际董事","董事会候选人"] 
f2 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\board_of_directors.txt","w+", encoding="utf-8") 
# 董事会下设机构
name_list3 = ["专业委员会委员","各专业委员会委员","战略委会委员","战略委员会委员","审计委员会委员","技术委员会委员","薪酬与考核委员会委员","提名委员会委员"] 
f3 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\board_of_directors1.txt","w+", encoding="utf-8") 
# 监事会
name_list4 = ["监事会主席","监事会副主席","监事"] 
f4 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\board_of_supervisors.txt","w+", encoding="utf-8") 
# 行政系统
name_list5 = ["总裁","副总裁","总经理","CEO","副总经理","总经理助理","办事机构负责人"] 
f5 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\administrative_system.txt","w+", encoding="utf-8") 
# 行政部门或事业部人员
name_list6 = ["证券部经理","技术负责人","客运销售代理人","财务顾问","法律顾问"]
f6 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\administrative_department_or_business_department_staff.txt","w+", encoding="utf-8") 
# 财务部门
name_list7 = ["财务负责人","CFO","会计","财务人员","财务总监","财务科长","财务部长"]
f7 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\financial_department.txt","w+", encoding="utf-8")  
# 内部审计部门
name_list8 = ["审计负责人","审计部门负责人","审计科长","审计部长","内部审计人员","审计部负责人"]
f8 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\internal_audit_department.txt","w+", encoding="utf-8")
# 外部审计机构
name_list9 = ["外部审计机构代表"]
f9 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\external_auditor.txt","w+", encoding="utf-8")
# 党委系统
name_list10 = ["党委","党组","党委书记","党委副书记","党委常委","党委委员"]
f10 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\party_committee_system.txt","w+", encoding="utf-8")
# 法律概念
name_list11 = ["实际控制人","法定代表人","授权代理人","失信被执行人"]
f11 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\legal_concept.txt","w+", encoding="utf-8")
# 泛称概念
name_list12 = ["高管","高级管理人员","核心管理人员","中层管理人员","核心技术人员","核心技术业务人员"]
f12 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\general_concept.txt","w+", encoding="utf-8")
# 其他
name_list13 = ["理事长","所长","副所长","委员","工程师","专家库专家","课题组长"]
f13 = open(r"E:\vscode-code\机器翻译\3.Target text reduction\other.txt","w+", encoding="utf-8")


# 依据类别写入相应的txt文件
def write_file (a:str):
    if (a==1):
        f1.write(line)
    elif (a==2):
        f2.write(line)
    elif (a==3):
        f3.write(line)
    elif (a==4):
        f4.write(line)
    elif (a==5):
        f5.write(line)
    elif (a==6):
        f6.write(line)
    elif (a==7):
        f7.write(line)
    elif (a==8):
        f8.write(line)
    elif (a==9):
        f9.write(line)
    elif (a==10):
        f10.write(line)
    elif (a==11):
        f11.write(line)
    elif (a==12):
        f12.write(line)
    else:
        f13.write(line)

# 判断当前文本所属类别
def judgment_category (b:str):
    if (line):
        if (any(name in line for name in name_list1)):
            return write_file(1)
        elif (any(name in line for name in name_list2)):
            return write_file(2)
        elif (any(name in line for name in name_list3)):
            return write_file(3)
        elif (any(name in line for name in name_list4)):
            return write_file(4)
        elif (any(name in line for name in name_list5)):
            return write_file(5)
        elif (any(name in line for name in name_list6)):
            return write_file(6)
        elif (any(name in line for name in name_list7)):
            return write_file(7)
        elif (any(name in line for name in name_list8)):
            return write_file(8)
        elif (any(name in line for name in name_list9)):
            return write_file(9)
        elif (any(name in line for name in name_list10)):
            return write_file(10)
        elif (any(name in line for name in name_list11)):
            return write_file(11)
        elif (any(name in line for name in name_list10)):
            return write_file(12)
        else:
            return write_file(13)

f = open(r"E:\vscode-code\机器翻译\2.Text merge+extraction\out_sen.txt","r")  
lines = f.readlines()#读取全部内容  
for line in lines: 
    #  .strip()消除指定字符 括号里不写，消除空格和换行符
    # print(line.strip())
    judgment_category(line)  

