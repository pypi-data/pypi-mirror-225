import os.path
import time

import numpy as np
import pandas as pd


# https://blog.csdn.net/Strive_For_Future/article/details/126710810

class obj:
    def __init__(
            self,
            path: str or None =None,  #            # 文件路径,如果不指定，则不保存
            index=None,         # 创建索引
            columns=None,       # 表头
            data=None,          # 数据，如果路径不存在，则提供数据，会新建文件
            json_orient=None,   # [json] 的读取与存储格式
            sheet_name=None,    # [excel] 表名
            mode:str or None=None,  # [csv] 写入方式，默认'w' 清空写入，'a' 追加写入
            **kwargs):
        self.path = path  # 建议.csv json，读写速度快
        self.index = index  # 设置索引，建议选择值没有重复的一列
        self.mode = mode
        self.file_extension = self.path.split(".")[-1] if self.path else None# 取文件扩展名

        # 如果没有指定路径，或者路径不存在
        if not self.path or not os.path.exists(self.path):
            if not data and not columns:    # 没有提供数据
                self.df = None
                return
            self.df = pd.DataFrame(data=data,columns=columns)   # 创建数据
            if self.path:
                self.save()
        else:
            if self.file_extension == "csv":
                self.df = pd.read_csv(
                    filepath_or_buffer=self.path,
                    header=0,   # [csv] 表头索引
                    encoding='utf-8',
                )    # convert_dates=False, keep_default_dates=False
            elif self.file_extension == "xlsx":
                self.sheet_name = sheet_name
                self.df = pd.DataFrame(pd.read_excel(self.path))
            elif self.file_extension == "json":
                self.json_orient = json_orient if json_orient else "split"  # orient 参数看下方注解，这里用split,节省空间
                r'''
                {"col1":{"0":"1","1":"3"},"col2":{"0":"2","1":"4"}}
                json_split =  {"columns":["col1","col2"],"index":[0,1],"data":[["1","2"],["3","4"]]} 
                json_records =  [{"col1":"1","col2":"2"},{"col1":"3","col2":"4"}] 
                json_index =  {"0":{"col1":"1","col2":"2"},"1":{"col1":"3","col2":"4"}} 
                json_columns =  {"col1":{"0":"1","1":"3"},"col2":{"0":"2","1":"4"}} 
                json_values =  [["1","2"],["3","4"]] 
                json_table =  {"schema":{"fields":[{"name":"index","type":"integer"},{"name":"col1","type":"string"},{"name":"col2","type":"string"}],"primaryKey":["index"],"pandas_version":"1.4.0"},"data":[{"index":0,"col1":"1","col2":"2"},{"index":1,"col1":"3","col2":"4"}]} 
                '''
                self.df = pd.read_json(path_or_buf=self.path,
                                       orient=self.json_orient,
                                       encoding='utf-8',
                                       dtype=False              # 自动判断数据类型
                                       )    # convert_dates=False, keep_default_dates=False
            else:
                self.df = pd.DataFrame(data=data)

        self.columns = columns if columns else self.df.columns.tolist()         # 获取表头
        self.set_index(self.index)      # 设置索引



    # 设置索引，
    def set_index(self, index=None):
        self.index = index if index is not None else self.index
        if not index or index[0]==None:
            self.df.reset_index(drop=True, inplace=True)
        else:
            self.df.set_index(index, drop=False, inplace=True)

    def add(self, data:dict,
            axis:0|1 =0     # 0 按行添加，纵向合并， 1 按列添加，横向合并
            ):
        df2 = pd.DataFrame(data=data,index=[self.index])
        self.df.reset_index(drop=True,inplace=True)     # 重置索引
        self.df = pd.concat([self.df, df2],axis=axis,ignore_index=True)     # ignore_index=True 是否忽略索引
        if self.index:
            self.set_index(self.index)
        return

    def save(self):
        if not self.path:
            return
        self.set_index()  # 先重置index，否则保存后无法读取
        self.file_extension = self.path.split(".")[-1] if self.path else None  # 取文件扩展名
        if self.columns:
            self.df = self.df[self.columns]
        if self.file_extension == "xlsx":
            self.df.to_excel(self.path, sheet_name=self.sheet_name,
                             index=False)  # index默认是True，导致第一列是空的,设置为False后可以去掉第一列。
        elif self.file_extension == "csv":
            mode = 'w' if self.mode is None else self.mode
            header = None if mode == 'a' else True     # 如果追加写入时，避免把表头追加进去，要设置表头为None,  True 全部表头，[a,..] 部分表头
            self.df.to_csv(path_or_buf=self.path,
                           header=header,
                           mode=mode,
                           index=False,         # 保存时不要索引
                           encoding="utf-8",
            )
        elif self.file_extension == "json":
            self.df.to_json(path_or_buf=self.path, orient=self.json_orient, date_format="iso",force_ascii=False)
            '''
            date_format:【None, ‘epoch’, ‘iso’】，日期转换类型。可将日期转为毫秒形式，iso格式为ISO8601时间格式。对于orient='table'，默认值为“iso”。对于所有其他方向，默认值为“epoch”
            double_precision:【int, default 10】,对浮点值进行编码时使用的小数位数。默认为10位。
            force_ascii:【boolean, default True】,默认开启，编码位ASCII码。
            date_unit:【string, default ‘ms’ (milliseconds)】,编码到的时间单位，控制时间戳和ISO8601精度。“s”、“ms”、“us”、“ns”中的一个分别表示秒、毫秒、微秒和纳秒.默认为毫秒。
            default_handler :【callable, default None】,如果对象无法转换为适合JSON的格式，则调用处理程序。应接收单个参数，该参数是要转换并返回可序列化对象的对象。
            lines：【boolean, default False】，如果“orient”是“records”，则写出以行分隔的json格式。如果“orient”不正确，则会抛出ValueError，因为其他对象与列表不同。
            compression:【None, ‘gzip’, ‘bz2’, ‘zip’, ‘xz’】，表示要在输出文件中使用的压缩的字符串，仅当第一个参数是文件名时使用。
            index:【boolean, default True】，是否在JSON字符串中包含索引值。仅当orient为“split”或“table”时，才支持不包含索引（index=False）。

            '''
        self.set_index(self.index)
    # 删除
    def drop(self,
             where,     # 条件 或者 行或列的标签名
             axis: 0 | 1 = 0,   # 0表示行，1 表示列
             ):
        '''

        :param where: dict {列名：内容}，int index,行号
        :return:
        '''
        if type(where) == dict:
            indexs = self.get_index(where)  # 取索引值
        else:  # where 是索引
            indexs = where if type(where) == list else [where]

        self.df.drop(labels=indexs, inplace=True,axis=axis)
        #self.df.reset_index(drop=True, inplace=True)  # 重新设置索引

    def get_index(self, where):
        '''

        :param where: dict {列名：内容}，int index,行号
        :return:[n,...]
        '''
        col = list(where.keys())[0]
        key = list(where.values())[0]
        indexs = self.df[self.df[col] == key].index.tolist()
        return indexs

    # 删除重复值
    def drop_duplicates(self, cols: list, keep="last", index=False, sort=True):
        '''
        cols：list 表示要进去重的列名，默认为 None。
        index: True,索引去重
        last：有三个可选参数，分别是 first、last、False，默认为 first，表示只保留第一次出现的重复项，删除其余重复项，last 表示只保留最后一次出现的重复项，False 则表示删除所有重复项。
        inplace：布尔值参数，默认为 False 表示删除重复项后返回一个副本，若为 Ture 则表示直接在原数据上删除重复项。
        :return:
        '''

        if index:
            self.drop_index_duplicates(keep)  # 索引去重，
        else:
            self.df.drop_duplicates(subset=cols, keep=keep, inplace=True)
        if sort:
            self.sort()

    # 索引去重
    def drop_index_duplicates(self, keep="last"):
        self.df = self.df[~self.df.index.duplicated(keep=keep)]

    def rename(self, cols: dict):
        '''

        :param cols: {原名：新名}
        :return:
        '''
        self.df = self.df.rename(columns=cols)

    # 数据替换
    def replace(  # type: ignore[override]
            self,
            value: str or list or dict,  # str 改单值，list 改一行 必须指定整行内容，dict 改这一行指定列的内容
            col: str or dict = None,  # 列名 或 列名：原值
            index: str or None = None,
    ) -> None:
        '''
        :param col:
        :param value:
        :param index:
        :return:
        '''

        if not index:
            old = list(col.values())[0]
            col = list(col.keys())[0]
            res = self.df.loc[(self.df[col] == old)]
            index = res.index.values[0]
        if type(value) == list:
            self.df.loc[index] = value
        elif type(value) == dict:
            for k, v in value.items():
                self.df.loc[index, k] = v
        else:
            self.df.loc[index, col] = value

    def sort(self, cols=False):
        '''
        如果不指定cols,则按索引重新排序
        :param cols: 可以是列表，也可以是字符串
        :return:
        '''
        if not cols:
            self.df.sort_index(inplace=True)
        else:
            self.df.sort_values(by=cols, inplace=True)

    def get(self, where=None, index=None, cols=None) -> object or None:
        '''
        where|index 只能指定其中一个

        1、使用“与”进行筛选
        df_inner.loc[(df_inner['age'] > 25) & (df_inner['city'] == 'beijing'), ['id','city','age','category','gender']]
        2、使用“或”进行筛选
        df_inner.loc[(df_inner['age'] > 25) | (df_inner['city'] == 'beijing'), ['id','city','age','category','gender']].sort(['age'])
        3、使用“非”条件进行筛选
        df_inner.loc[(df_inner['city'] != 'beijing'), ['id','city','age','category','gender']].sort(['id'])
        4、对筛选后的数据按city列进行计数
        df_inner.loc[(df_inner['city'] != 'beijing'), ['id','city','age','category','gender']].sort(['id']).city.count()
        5、使用query函数进行筛选
        df_inner.query('city == ["beijing", "shanghai"]')
        6、对筛选后的结果按prince进行求和
        df_inner.query('city == ["beijing", "shanghai"]').price.sum()
        :param where: 可以是dict条件，也可以是索引，也可以是False表示全部
        :return: {}
        '''
        try:
            if index:  # 按索引取值
                return self.df.loc[index] if not cols else self.df.loc[index, cols]
            elif where is not None: # 按条件语句取值
                return self.df.loc[where] if not cols else self.df.loc[where, cols]
            elif not where and not index:
                return self.df
        except:
            return None # 没有此值，没有找到结果


    #

    # 1、维度查看：
    # self.df.shape     # 返回（r,c） 几行几列,列头是0行

    # 2、数据表基本信息（维度、列名称、数据格式、所占空间等）：
    # self.df.info()

    # 3、查看所有行的行索引名
    # self.df.index           # 得到一个对象
    # self.df.index.values    # 得到一个列表

    # 4、查看所有列的列索引名
    # 查看所有列的列名
    # self.df.columns  # 得到的是一个series对象
    # self.df.columns.values  # 得到的是一个列表

    # 5、定位表格中的指定元素
    # 要在pandas.DataFrame中的任何位置检索或更改数据，可以使用at，iat，loc，iloc。
    # 更多细节详见 https://blog.csdn.net/qq_18351157/article/details/104838924
    # print(self.df.at['行标签名', '列标签名'])
    # print(self.df.iat['行索引号', '列索引号'])

    # print(self.df.loc['行标签名', '列标签名'])
    # print(self.df.iloc[行索引数字, 列索引数字])

    # print(self.df.loc['行标签名1':'行标签名2', '列标签名1': '列标签名2'])
    # print(self.df.iloc[行索引数字1:行索引数字2, 列索引数字1:列索引数字2])

    # 6、每一列数据的格式：
    # self.df.dtypes

    # 7、某一列格式：
    # self.df['B'].dtype

    # 8、查看某一列的所有值
    # self.df["姓名"].values  # 获取某一列的所有数值
    # 说明:需要先用对应列的列名称“姓名”获取对应列对象，然后用.values将对象转变为列表



