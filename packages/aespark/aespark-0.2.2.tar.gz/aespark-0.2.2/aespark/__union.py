import pandas as pd
from pathlib import Path
from tqdm import tqdm
import jieba
from .__dataclean import *
import os

def union_sheet(url: str, limit: int = 42000000, link: bool = False, lex: str = '*'):
    '''
    功能简介：
        合并单个sheet的文件；
    参数解释：
        url     目标文件夹路径(文件夹中只能有.csv.xls或.xlsx格式的文件)；
        limit   输出表容量（多少条数据存一张表；默认80万行）；
        link    是否需要添加数据来源，默认不添加；
        lex     需要合并的文件后缀，默认为所有；
    '''
    files = pd.DataFrame(columns=['文件名称', '文件路径'])
    geshi = pd.DataFrame(columns=['总文件名', '表格式', '文件数量'])

    for i in Path(url).rglob(f'*.{lex}'):
        files.loc[len(files)] = [Path(i).stem, i]

    for i in tqdm(files.index, desc='数据提取'):

        if lex == '*':
            filelex = str(files['文件路径'][i])
            iii = filelex[filelex.rindex('.'):]
            if 'xls' in iii or 'xlsx' in iii:
                df = pd.read_excel(files['文件路径'][i], dtype='str')
            elif 'csv' in iii:
                df = pd.read_csv(files['文件路径'][i],
                                 dtype='str', encoding='gb18030')
        elif lex in ['xls', 'xlsx']:
            df = pd.read_excel(files['文件路径'][i], dtype='str')
        elif lex == 'csv':
            df = pd.read_csv(files['文件路径'][i], dtype='str', encoding='gb18030')

        if link:
            df['原始文件路径'] = files['文件路径'][i]
        lis = df.columns.to_list()
        lis.sort()
        lis = ''.join(lis)

        if lis in list(geshi['表格式']):
            row_index = geshi[geshi['表格式'] == lis].index.tolist()[0]
            geshi['总文件名'][row_index] += files['文件名称'][i]
            geshi['文件数量'][row_index] += 1
            exec(f"hebin{row_index} = pd.concat([hebin{row_index}, df])")
        else:
            exec(f"hebin{len(geshi)} = df.copy()")
            geshi.loc[len(geshi)] = [files['文件名称'][i], lis, 1]

    geshi['总文件名'] = geshi['总文件名'].str.replace(
        '[^\u4e00-\u9fa5]', '', regex=True)

    for i in tqdm(geshi.index, desc='数据产出'):

        if geshi['总文件名'][i] != '':
            result = jieba.tokenize(geshi['总文件名'][i])
            cutresult = pd.DataFrame(columns=['word', 'start'])
            for tk in result:
                cutresult.loc[len(cutresult)] = [tk[0],tk[1]]
            cutresult = cutresult.pivot_table(index='word', values='start', aggfunc=['count', 'sum']).reset_index()
            cutresult.columns = ['word', 'count', 'start']
            cutresult.sort_values(by=['count', 'start'], ascending=[False, True], inplace=True)
            cutresult = cutresult[cutresult['count']==cutresult['count'].max()]
            file_name = ''.join(list(cutresult['word']))
        else:
            file_name = '未知'

        exec(f"hebin{i}.drop_duplicates(inplace=True)")
        exec(f"hebin{i}.reset_index(drop=True, inplace=True)")
        exec(f"hebin{i} = dc_invisCharDel(hebin{i}, df=True)")
        exec(f"hebin{i} = dc_excelAddT(hebin{i})")

        n = ''
        num = geshi['文件数量'][i]
        all = geshi['文件数量'].sum()
        buildFolder('合并数据产出')
        while eval(f"len(hebin{i})") > limit:
            n = 1 if n == '' else n+1
            exec(f"hebin{i}.loc[:{limit}].to_csv(r'合并数据产出\{i+1}.{file_name}({num},总{all}){n}.csv', index=False, encoding='gb18030')")
            exec(f"hebin{i} = hebin{i}.loc[{limit+1}:]")
            exec(f"hebin{i}.reset_index(drop=True, inplace=True)")

        exec(
            f"hebin{i}.to_csv(r'合并数据产出\{i+1}.{file_name}({num},总{all}){n}.csv', index=False, encoding='gb18030')")

def union_sheets(url: str, lex: str = '*', link: bool = False, seq: str = '_', ind: int = None, save:bool = True):
    '''
    功能简介：
        按sheet名称合并多个excel文件；
    功能输出：
        一个含有多个dataframe的数组；
    参数解释：
        url     文件夹路径；
        lex     需要合并的文件后缀，默认为所有，如果目标文件夹内有其他类型文件需要设定；
        link    是否需要标记数据来源；
        seq     文件名称分隔符，默认为"_"；
        ind     来源位于文件名称第几个，起始为"0"，缺省时添加文件名称为来源；
    '''
    files = [str(i) for i in Path(url).rglob(f'*.{lex}')]  # 获取目标文件夹下的所有文件路径
    for file in tqdm(files, desc='数据抽取'):
        df = pd.read_excel(file, sheet_name=None,
                           keep_default_na='', dtype='str')
        sheets = list(df.keys())

        if link:  # 若选择了标记数据来源，则给所有sheet内的数据行添加来源内容
            if ind == None:
                lin = file[file.rfind('\\')+1:file.rfind('.')]
            else:
                lin = file[file.rfind('\\')+1:file.rfind('.')].split(seq)[ind]
            for i in range(len(sheets)):
                df[sheets[i]]['数据来源'] = lin

        if 'first' not in locals():
            alldata = df  # 存放所有sheet，用于最终输出
            first = 1
        else:
            for sheet in sheets:  # 按sheet合并
                try:
                    alldata[sheet] = pd.concat([alldata[sheet], df[sheet]])
                except:
                    alldata[sheet] = pd.DataFrame()
                    alldata[sheet] = pd.concat([alldata[sheet], df[sheet]])

    for sheet in list(alldata.keys()):
        alldata[sheet].drop_duplicates(inplace=True)
        alldata[sheet].reset_index(inplace=True, drop=True)

    if save == False:
        print(f"合并完成：共得到{len(alldata.keys())}个表格：{'、'.join([i for i in alldata.keys()])}")
    else:
        buildFolder('多sheet合并数据产出')
        with pd.ExcelWriter(f"多sheet合并数据产出/多sheet合并结果.xlsx") as score_file:
            for sheet in list(alldata.keys()):
                alldata[sheet].to_excel(score_file,sheet_name = sheet, index = False)

    return alldata

def buildFolder(url: str):
    '''
    功能简介：
        根据传入路径创建文件夹，自动跳过已存在文件夹；
    所需参数：
        路径，可以是多层文件夹；
    return：
        路径创建情况；
    '''
    if '\\' in url:
        url = url.replace('\\', '/')

    for i in url.split('/'):
        if 'urlstr' not in locals():
            urlstr = i
        else:
            urlstr += '/'+i
        if os.path.exists(urlstr) is False:
            os.mkdir(urlstr)