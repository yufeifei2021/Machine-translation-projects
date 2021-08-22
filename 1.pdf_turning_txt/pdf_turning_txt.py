import time,os.path,re
import pdfplumber
import pandas as pd
from decimal import *
import xml.dom.minidom as minidom

class pdfText:
    top = 55
    bottom = 800
    def __init__(self, pages):
        self.part_pages = []
        self.marks = []
        for page in pages:
            p, m = self.seperate_table(page)
            self.part_pages.extend(p)
            self.marks.extend(m)
        l, r = self.find_margin(pages[0])
        self.lines, self.tables_text = self.read_pdf(l, r)
    
    def seperate_table(self, page):
        bottom = min(self.bottom, page.height)
        mark = []
        new_pages = []
        tables = page.find_tables() # 获取所有表格
        page_box = (Decimal(0), Decimal(self.top), Decimal(page.width), Decimal(bottom))

        for table in tables:
            if page_box[1] > table.bbox[1]:
                print("异常表格")
                break
            new_page = page.crop((page_box[0], page_box[1], page_box[2], table.bbox[1])) # 先切出表格上部   # -Decimal(0.1) 是否考虑表格边缘
            new_pages.append(new_page)                                       # 未筛选切处的空白页
            mark.append(False)
            new_page = page.crop((page_box[0], table.bbox[1], page_box[2], table.bbox[3])) # 切出表格
            new_pages.append(new_page)
            mark.append(True)
            page_box = (page_box[0], table.bbox[3], page_box[2], page_box[3]) # 调整page_box范围为剩余部分页面
            # print(rest_box)
        new_pages.append(page.crop(page_box)) # 加上剩余部分页面
        mark.append(False)
        return new_pages, mark

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def find_margin(self, page):
        x0 = []
        x1 = []
        for i in range(min(250, len(page.chars))): # 根据前250字坐标位置极限确定边距
            ch = page.chars[i]["text"]
            if '\u4e00' <= ch <= '\u9fff':
                x0.append(page.chars[i]["x0"])
                x1.append(page.chars[i]["x1"])
        return min(x0), max(x1)

    def merge_lines(self, lines, page, l, r):
        need_divide_lines = [] # 需换行的行序号
        new_text = ""
        
        # chars_order = sorted(page.chars,key=lambda x:(-x["y0"], x["x0"]),reverse=False)
        chars = "".join([x["text"] for x in page.chars]) # 全页字符
        start = 0
        # print(chars)
        temp = 0
        for i, line in enumerate(lines):
            
            # line = line.replace(" ", "") # chars中很多地方忽略了空格
            if len(line) > 6: # 一行大于6字时可能需要换行
                # 取一行内前六个字和后六个字在全页中寻找位置
                index1 = chars.find(line[-6:], start)
                index2 = chars.find(line[:6], start)
                # print(line)
                # print(index1, index2)
                
                # if index1 < 0 or index2 < 0:
                #     print("cant find text!", line, chars[start:start+5])
                # else:
                #     start = index2

                if index2 > 0:
                    start = index2
                
                if index1 >= 0 and r-page.chars[index1+5]["x1"]>12: # 后六个字中的最后一个字离右边界距离大于12则大概率需要换行
                        need_divide_lines.append(i)
                        # print(i, "tail")
                
                # if index2 > 0 and page.chars[index2]["x0"]>l+11: # 前六个字的第一个字距离左边界大于11则大概率需要换行
                #     if i > 0:
                #         need_divide_lines.append(i-1)
                #     # print(i, "begin")

            else:
                need_divide_lines.append(i)
                start += len(line)
            # start += len(line) # 从后一句开始寻找字符的位置

        for i, line in enumerate(lines):
            new_text += line
            if i in need_divide_lines:
                new_text += "\n"
        new_text = new_text.replace("。", "。\n").replace(";", ";\n").replace("；", "；\n").replace(" ", "")
        return new_text

    # 读取pdf文字内容，并处理多余换行，返回各行文字组成的list
    def read_pdf(self, x0, x1):
        all_lines_text = ""
        all_tables_text = []
        for num, page in enumerate(self.part_pages):
            if self.marks[num]:
                all_tables_text.append(page.extract_text().split(" "))
                continue
            text = page.extract_text()
            if not text:
                continue
            lines = text.split("\n")
            lines_text = self.merge_lines(lines, page, x0, x1)
            all_lines_text += lines_text
        all_lines = all_lines_text.split("\n")
        
        index_to_delete = []
        for i, x in enumerate(all_lines):
            if not x or x.isspace(): # 去除空行
                        index_to_delete.append(i)
            # elif len(x.strip())<4 and is_number(x): # 去除页码
            #             index_to_delete.append(i)
        all_lines = [all_lines[i] for i in range(0, len(all_lines), 1) if i not in index_to_delete]
        return all_lines, all_tables_text

    def get_lines(self):
        return self.lines
    
    def get_tables(self):
        return self.tables_text
        
if __name__ == '__main__':
    path = 'E:/vscode-code/机器翻译/1.pdf_turning_txt/sample/'
    out_path = 'E:/vscode-code/机器翻译/1.pdf_turning_txt/out/'
    data_file_list = os.listdir(path)
    for file in data_file_list:
        try:
            with pdfplumber.open(path+file) as pdf:
                Text = pdfText(pdf.pages)
                file_lines = Text.get_lines()
                table_text = Text.get_tables()
            with open(out_path+file[:-3]+"txt", "w", encoding="utf-8") as f:
                for line in file_lines:
                    f.write(line + "\n")
                for row in table_text:
                    f.write("".join(row) + "\n")
        except Exception as e:
            print(file, e)

 