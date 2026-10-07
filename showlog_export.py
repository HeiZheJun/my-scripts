# -*- encoding:utf8 -*-

#   读取慢日志文件，导出为excel，csv文件格式。
#   目前支持mysql5.7版本，其他版本可能会出现问题



import re
import sys
import os
from datetime import datetime as dt
import argparse
import openpyxl


def export_data():
    parse = argparse.ArgumentParser(description="慢日志导出脚本",add_help=False)
    parse.add_argument('-f', '--file', help="读取文件路径", default="mysqld_slow.log")
    parse.add_argument('-t', '--type', help="导出文件类型，默认CSV", default="xlsx", choices=["csv","xlsx"])
    parse.add_argument('-o', '--out', help="导出路径", type=str, default='showlog')
    parse.add_argument('-h', '--help', action='help',   help='显示帮助信息并退出')
    args = parse.parse_args()
    return args


class ExcelWriter:
    def __init__(self,filename: str, headers: list = ["执行时间","数据库用户","认证用户","连接IP","连接ID","查询时间","锁表时间","返回行数","扫描行数","执行SQL"]):
        """初始化openpyxl""" 
        self.filename = filename if filename.endswith(".xlsx") else f"{filename}.xlsx"
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.active
        self.sheet.title = "慢日志明细"
        self.sheet.append(headers)

    def write_row(self, row_data):
        """写入一行文件"""
        try:
            self.sheet.append(row_data)
        except Exception as error:
            print(error)
            sys.exit(1)

    def close_row(self):
        """保存关闭文件"""
        self.wb.save(self.filename)

class CsvlWriter:
    def __init__(self,filename: str, headers: str = "执行时间,数据库用户,认证用户,连接IP,连接ID,查询时间,锁表时间,返回行数,扫描行数,执行SQL\n"):
        """创建csv文件并写入表头"""
        self.filename = filename if filename.endswith(".csv") else f"{filename}.csv"
        self.cf = open(self.filename, 'w', encoding="utf8")
        self.cf.write(headers)

    def write_row(self, row_data):
        """写入一行文件"""
        try:
            self.cf.write(row_data)
        except Exception as error:
            print(error)
            sys.exit(1)

    def close_row(self):
        """保存关闭文件"""
        self.cf.close()


class DataProcess:
    def __init__(self, filename):
        """验证文件并设置过滤正则表达式"""
        if not (os.path.exists(filename) and os.path.isfile(filename)):
            raise FileNotFoundError(f"无效文件路径或文件不存在: {filename}")
        self.filename = filename
        self.RE_TIME = r'^# Time:\s*(\S+)'
        self.RE_USER = r'^# User@Host:\s*(\S*)\[(.*?)\]\s*@\s*\[(.*?)\]\s*Id:\s*(\d+)'
        self.RE_QUERY = r'^# Query_time:\s*([\d.]+)\s*Lock_time:\s*([\d.]+)\s*Rows_sent:\s*([\d.]+)\s*Rows_examined:\s*([\d.]+)'
        self.RE_SQL = r"^[^#].*"

    def __time_convert(self, start_time):
        """
            转换时间格式为%Y-%m-%d %H:%M:%S
            示例： 2026-10-06T06:14:35.292953Z -> 2025-10-06 06:14:35
        """
        try:
            return dt.strftime(dt.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ"), "%Y-%m-%d %H:%M:%S")
            
        except Exception as error:
            print(error)
            sys.exit(1)

    def process_data(self):
        """处理读取到的文件数据"""
        process = []
        sql_process = []
        sql_line = ''
        with open(self.filename, 'r', encoding='utf8') as f:
            while True:
                line = f.readline()
                if not line:
                    break

                # 匹配开始时间行，匹配新任务之后，把之前的任务写入变量，初始化任务变量
                filter_result = re.match(self.RE_TIME, line)
                if filter_result:
                    start_time = self.__time_convert(filter_result.group(1))
                    if sql_line == '':
                        sql_process.append(start_time)
                    else:
                        sql_process.append(sql_line)
                        process.append(sql_process)
                        sql_line = ''
                        sql_process = []
                        sql_process.append(start_time)

                # 匹配用户信息行
                filter_result = re.match(self.RE_USER, line)
                if filter_result:
                    sql_process.extend([filter_result.group(i) for i in range(1,5)])

                # 匹配查询信息行
                filter_result = re.match(self.RE_QUERY, line)
                if filter_result:
                    sql_process.extend([filter_result.group(i) for i in range(1,5)])

                # 匹配执行sql
                filter_result = re.match(self.RE_SQL, line)
                if filter_result:
                    sql_line = sql_line + filter_result.group(0) + "\n"
        return process


def check_path(path):
    """
        检测文件路径是否存在，如果不存在则创建对应的路径
    """
    if os.path.sep in path and  not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def main():
    #  加载参数
    args = export_data()

    # 检查导出文件路径
    check_path(args.out)
    print(args.out)
    # 初始化数据过滤，并格式化输出
    dp = DataProcess(args.file)
    result = dp.process_data()

    # 导出
    if args.type == "csv":
        csv = CsvlWriter(args.out)
        for sql_task in result:
            sql = f'"{sql_task[-1]}"'
            task_info = str(sql_task[:-1]).strip('[]').replace("'","") + "," + sql + "\n"
            csv.write_row(task_info)
        csv.close_row()

    elif args.type == "xlsx":
        xlsx = ExcelWriter(args.out)
        for sql_task in result:
            xlsx.write_row(sql_task)
        xlsx.close_row()




if __name__ == '__main__':
    main()
