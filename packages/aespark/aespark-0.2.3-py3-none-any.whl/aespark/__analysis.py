import pandas as pd
from .__dataclean import *

class Palette():

    def __init__(self) -> None:
        self.palette = pd.DataFrame(columns=['主端'])

    def add_color(self, main:str, col:str|list, color:str|int|float|list):
        '''
        功能简介：
            在情况汇总表上作上一个记录
        参数解释：
            main    记到谁的头上
            col 记录的项目名称是什么（即列名），可以是列表，但必须与color数量一致；
            color   需要记录的内容是什么，可以是列表，但必须与col数量一致；
        使用举例：
            add_color('李四', '花呗记录', '有')；
            add_color('张三', ['余额宝', '花呗记录'], [986.32, '有'])；
        '''
        if type(col) != list:
            col = [col]
            color = [color]
        if len(col) != len(color):
            raise Exception('项目(col)与内容(color)的数量需要一致')
        if main not in list(self.palette['主端']):
            self.palette.loc[len(self.palette)] = {'主端':main}
        for i in range(len(col)):
            if col[i] not in self.palette.columns.to_list():
                self.palette = pd.concat([self.palette, pd.DataFrame(columns=[col[i]])])
            ind = list(self.palette[self.palette['主端']==main].index)[0]
            self.palette[col[i]][ind] = color[i]

    def save(self, url:str='palette-未设置保存名称.xlsx'):
        self.palette['主端'] = self.palette['主端'].astype('str')
        self.palette.to_excel(url, index=False)

def piv_transView(df:pd.DataFrame, collist:list):
    '''
    功能简介：
        基于交易数据产出账户交易概况表；
    参数解释：
        df  交易数据表；
        collist 字段列表，顺序需要一致，[主端账户，交易金额，借贷标志，交易时间]；
    调用示例：
        pivdf = piv_transView(df,['用户ID', '金额(元)', '收/支', '创建时间'])；
    '''
    df = df[[collist[0],collist[1], collist[2], collist[3]]]
    df = dc_amClean(df, collist[1])
    df[collist[2]] = df[collist[2]].apply(dc_inOutClean)
    df[collist[3]] = df[collist[3]].apply(dc_Time)
    if '进' not in list(df[collist[2]].drop_duplicates()) or '出' not in list(df[collist[2]].drop_duplicates()):
        df.loc[len(df)] = ['填充用账户', 0, '进', '1999.01.01 11:14:42']
        df.loc[len(df)] = ['填充用账户', 0, '出', '1999.01.01 11:14:42']
    piv = df.pivot_table(index=collist[0], columns=collist[2], values=collist[1], aggfunc=['sum', 'count']).reset_index()
    piv.columns = [''.join([i[1],i[0]]).replace('sum', '金额').replace('count', '次数') for i in piv.columns]
    if '填充用账户' in list(piv[collist[0]]):
        piv.drop(piv[piv[collist[0]]=='填充用账户'].index, inplace=True)
    if len(piv.columns) == 7:
        piv = piv.take([0, 1, 4, 2, 5, 3, 6], axis=1)
    else:
        piv = piv.take([0, 1, 3, 2, 4], axis=1)
    piv.fillna(0, inplace=True)
    piv['总金额'] = piv['其他金额']+piv['出金额']+piv['进金额'] if len(piv.columns) == 7 else piv['出金额']+piv['进金额']
    df[collist[3]] = pd.to_datetime(df[collist[3]])
    piv2 = df.pivot_table(index=collist[0], values=collist[3], aggfunc=['min', 'max']).reset_index()
    piv2.columns = [collist[0], '首次交易', '末次交易']
    piv2['首次交易'] = piv2['首次交易'].apply(lambda x:str(x)[:str(x).index(' ')].replace('-','.'))
    piv2['末次交易'] = piv2['末次交易'].apply(lambda x:str(x)[:str(x).index(' ')].replace('-','.'))

    piv = pd.merge(left=piv, right=piv2, how='left', on=collist[0])
    for i in piv.columns:
        if '金额' in i:
            piv[i] = piv[i].apply(lambda x: '%.2f'%x)
        elif '次数' in i:
            piv[i] = piv[i].astype('int')
    piv.sort_values(by=['总金额', '末次交易', '首次交易'], ascending=[False, False, True], inplace=True)

    return piv