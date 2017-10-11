#encoding=utf-8
import os

import xlwt, xlrd
from xlutils.copy import copy
from datetime import datetime
from xlwt.Style import XFStyle
from logic.utility import *

Download_Location = "/tmp/"
class ExcelWrite():
    def __init__(self):
        self.work_book = xlwt.Workbook()
        self.sheet = self.work_book.add_sheet("Sheet1")
        if not os.path.exists(Download_Location):
            os.mkdir(Download_Location)
        self.file_name = "{}/{}.xls".format(
                                        Download_Location,
                                            datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    def write(self, title, data):
        """
        title: ['', '']
        data:  [['', '', ''], ['', '', '']]
        """
        for col, t in enumerate(title):
            cwidth = self.sheet.col(col).width

            self.sheet.write(0, col, t.decode('utf8'))

            if (len(t)*256) > cwidth:
                self.sheet.col(col).width = (len(t)*256)

        for row, d in enumerate(data):
            for col, _d in enumerate(d):
                cwidth = self.sheet.col(col).width

                try:
                    _d = str(_d)
                    self.sheet.write(row + 1, col, _d.decode('utf8'))
                    if (len(_d)*256) > cwidth and len(_d)*256 < 65535:
                        self.sheet.col(col).width = (len(_d)*256)
                except:
                    pass

        self.work_book.save(self.file_name)

        return self.file_name


class ExcelRead():
    def __init__(self, file_name):
        self.work_book = xlrd.open_workbook(file_name)

    def get_data(self):
        data = []
        sheet = self.work_book.sheet_by_index(0)
        nrows = sheet.nrows
        ncols = sheet.ncols
        for i in range(nrows):
            data.append(sheet.row_values(i))

        return data

if __name__=="__main__":
    excelWriter = ExcelWrite()
    title=['a','b']
    data=[['1','2'],['3','4']]
    print excelWriter.write(title, data)
