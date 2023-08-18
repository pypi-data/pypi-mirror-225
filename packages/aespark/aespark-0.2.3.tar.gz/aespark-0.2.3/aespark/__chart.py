from typing import Literal
from pyecharts.charts import *
from pyecharts import options as opts
import pandas as pd
import datetime
import jieba
from .__dataclean import *
import pkg_resources


def chart_calendar(df:pd.DataFrame, crtime:str, money:str, url:str='交易金额分布-日历图.html', clist:list=[0, 1000, 5000, 20000, 50000], flexible:Literal['max', 'average', 'count']='', save:bool=True):
    '''
    功能介绍：
        基于交易数据产出交易金额分布图（日历图）；
    参数解释：
        df 交易信息表；
        crtime 交易时间-列名；
        money 交易金额-列名；
        url 产出材料保存路径；
        clist 资金阶级，五个整数的数组；
        flexible 是否根据不同情况自动划分资金阶级(max:按最大值，average:按平均值，count:按次数)；
        save 是否要产出文件
    '''
    df[crtime]=df[crtime].astype(str)
    df[crtime] = df[crtime].apply(dc_Time)
    df = df[df[crtime].notna()]
    if len(df)==0:
        raise Exception('error: No valid data found.')
    begin = datetime.datetime.strptime(df[crtime].min(),'%Y.%m.%d %H:%M:%S')
    end = datetime.datetime.strptime(df[crtime].max(),'%Y.%m.%d %H:%M:%S')
    df['time'] = df[crtime].apply(lambda x:datetime.datetime.strptime(x,'%Y.%m.%d %H:%M:%S').strftime('%Y-%m-%d'))
    piv = df.pivot_table(index='time', values=money, aggfunc='sum').reset_index()
    data = [
        [(begin + datetime.timedelta(days=i)).strftime('%Y-%m-%d'), round(list(piv[piv['time']==(begin + datetime.timedelta(days=i)).strftime('%Y-%m-%d')][money])[0],2) if len(piv[piv['time']==(begin + datetime.timedelta(days=i)).strftime('%Y-%m-%d')]) != 0 else 0]
        for i in range((end - begin).days + 1)
    ]
    if flexible != '':
        if flexible == 'max':
            line = pd.DataFrame(data)[1].max()
            clist = [0, int(line*0.1), int(line*0.3), int(line*0.5), int(line*0.8)]
        elif flexible == 'average':
            line = pd.DataFrame(data)[1].sum()/len(data)
            clist = [0, int(line*0.3), int(line*0.5), int(line), int(line*1.5)]
        elif flexible == 'count':
            d = pd.DataFrame(data)
            lis = d[d[1]>=1][1].to_list()
            lis.sort()
            clist = [0, int(lis[int(len(lis)*0.2)]), int(lis[int(len(lis)*0.4)]), int(lis[int(len(lis)*0.7)]), int(lis[int(len(lis)*0.92)])]
    calendar = (
        Calendar()
        .add(
            "",
            data,
            calendar_opts=opts.CalendarOpts(
                range_=[begin,end],
                daylabel_opts=opts.CalendarDayLabelOpts(name_map="cn"),
                monthlabel_opts=opts.CalendarMonthLabelOpts(name_map="cn"),
            ),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="交易金额分布"),
            visualmap_opts=opts.VisualMapOpts(
                max_=int(piv[money].max())+1,
                min_=0,
                orient='horizontal',
                is_piecewise=True,
                pos_top="230px",
                pos_left="100px",
                pieces=[
                    {"min": clist[0]+0.01, "max": clist[1], "label": f"{format(clist[0],',')}~", 'color': '#C5E9FF'},
                    {"min": clist[1], "max": clist[2], "label": f"{format(clist[1],',')}~", 'color': '#63DBF7'},
                    {"min": clist[2], "max": clist[3], "label": f"{format(clist[2],',')}~", 'color': '#1B9AEE'},
                    {"min": clist[3], "max": clist[4], "label": f"{format(clist[3],',')}~", 'color': '#006CFA'},
                    {"min": clist[4], "max": int(piv[money].max())+1, "label": f"{format(clist[4],',')}~", 'color': '#003F92'},
                ]
            ),
        )
    )
    if save is False:
        return calendar
    else:
        calendar.render(url)

def chart_wordcloud(df:pd.DataFrame, inf:str|list, url:str='交易画像-词云.html', ignore:str|list='', save:bool=True):
    '''
    功能介绍：
        基于交易信息产出交易画像，大体掌握账户性质信息；
    参数解释：
        df 交易数据表
        inf 需要纳入统计的列名，有多个时以数组方式输入；
        url 产出文件保存路径
        ignore 在最终词云上忽略特定词语，有多个时以数组方式输入；
        save 是否要产出文件
    '''
    dist = pkg_resources.get_distribution("aespark")
    jieba.load_userdict (f'{dist.location}/aespark/static/jieba_word.txt')

    if type(inf) is str:
        strs = ''.join(df[inf].to_list())
    else:
        strs = ''
        for i in inf:
            strs += ''.join(df[i].to_list())

    d = pd.DataFrame(pd.DataFrame(jieba.cut(re.sub('[^\u4e00-\u9fa5]', '', strs))).groupby(0).size())
    
    d.columns=[1]
    d.reset_index(inplace=True)
    d.sort_values(1,ascending=False,inplace=True)
    if ignore != '':
        if type(ignore) is str:
            d.drop(d[d[0]==ignore].index, inplace=True)
        else:
            for i in ignore:
                d.drop(d[d[0]==i].index, inplace=True)
    d.reset_index(inplace=True, drop=True)

    if len(d) == 0:
        raise Exception('error: No valid data found.')
    
    d = d.loc[:100]
    words = []
    for i in d.index:
        words.append((str(d[0][i]), int(d[1][i])))

    wordcloud = (
        WordCloud()
        .add("", words, word_size_range=[12, 48])
        .set_global_opts(title_opts=opts.TitleOpts(title="交易画像"))
    )
    if save is False:
        return wordcloud
    else:
        wordcloud.render(url)

def chart_sumcount(df:pd.DataFrame, crtime:str, money:str, url:str = '交易规律图-复合图.html', save:bool=True):
    '''
    功能介绍：
        基于交易记录表，产出分时、分日的交易规律图，展现交易金额及次数；
    参数解释：
        df 交易记录表；
        crtime 交易时间-列名；
        money 交易金额-列名；
        url 产出材料保存路径；
        save 是否要保存成文件，默认保存
    '''
    df[crtime] = df[crtime].astype(str)
    df[crtime] = df[crtime].apply(dc_Time)
    df = dc_amClean(df, money)
    df = df[df[crtime].notna()]
    if len(df)==0:
        raise Exception('error: No valid data found.')

    df['day'] = df[crtime].apply(lambda x:datetime.datetime.strptime(x,'%Y.%m.%d %H:%M:%S').day)
    df['hour'] = df[crtime].apply(lambda x:datetime.datetime.strptime(x,'%Y.%m.%d %H:%M:%S').hour)

    def __chart_out(dom:str, x_data:list):
        piv = df.pivot_table(index=dom, values=money, aggfunc=['sum', 'count']).reset_index()
        piv.columns = ['day', 'sum', 'count']

        for i in x_data:
            if i not in list(piv['day']):
                piv.loc[len(piv)] = [i,0,0]
        piv.sort_values('day', ascending=True, inplace=True)

        y_count = list(piv['count'])
        y_sum = list(piv['sum'])

        bar = (
            Bar()
            .add_xaxis(x_data)
            .add_yaxis('金额', y_sum)
            .extend_axis(
                yaxis=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter='{value} 次')
                )
            )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                    title_opts=opts.TitleOpts(title=f'交易规律-{dom}'),
                    yaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(formatter="{value} 元")
                    ),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(
                            is_show=True, position="top", rotate=15, interval=0
                        )
                    ),
            )
        )
        line = (
            Line().add_xaxis(x_data).add_yaxis("次数", y_count, yaxis_index=1, z_level=1)
        )
        bar.overlap(line)
        return bar

    bar_hour = __chart_out('hour', [i for i in range(1,25)])
    bar_day = __chart_out('day', [i for i in range(1,32)])
    if save:
        page = Page(layout=Page.SimplePageLayout)
        page.add(
            bar_hour,
            bar_day,
        )
        page.render(url)
    else:
        return [bar_hour,bar_day]