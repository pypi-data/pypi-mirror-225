from pyecharts.charts import *
from pyecharts import options as opts
import pandas as pd
import datetime
from .__dataclean import *

def calendar(df:pd.DataFrame, crtime:str, money:str, clist:list=[0, 3000, 10000, 30000, 70000]):
    '''
    功能介绍：
        基于交易数据产出交易金额分布图（日历图）
    参数解释：
        df 交易信息表
        crtime 交易时间-列名
        money 交易金额-列名
        clist 资金阶级，五个整数的数组
    '''
    begin = datetime.datetime.strptime(dc_Time(df[crtime].min()),'%Y.%m.%d %H:%M:%S')
    end = datetime.datetime.strptime(dc_Time(df[crtime].max()),'%Y.%m.%d %H:%M:%S')
    df['time'] = df[crtime].apply(lambda x:datetime.datetime.strptime(dc_Time(x),'%Y.%m.%d %H:%M:%S').strftime('%Y-%m-%d'))
    piv = df.pivot_table(index='time', values=money, aggfunc='sum').reset_index()
    data = [
        [str(begin + datetime.timedelta(days=i))[:10], round(list(piv[piv['time']==str(begin + datetime.timedelta(days=i))[:10]][money])[0],2) if len(piv[piv['time']==str(begin + datetime.timedelta(days=i))[:10]]) != 0 else 0]
        for i in range((end - begin).days + 1)
    ]
    (
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
                    {"min": clist[0], "max": clist[1], "label": f"~{format(clist[0],',')}", 'color': '#D9D9D9'},
                    {"min": clist[1], "max": clist[2], "label": f"{format(clist[1],',')}~", 'color': '#C5E9FF'},
                    {"min": clist[2], "max": clist[3], "label": f"{format(clist[2],',')}~", 'color': '#63DBF7'},
                    {"min": clist[3], "max": clist[4], "label": f"{format(clist[3],',')}~", 'color': '#1B9AEE'},
                    {"min": clist[4], "max": int(piv[money].max())+1, "label": f"{format(clist[4],',')}~", 'color': '#006CFA'},
                ]
            ),
        )
    ).render('交易金额分布-日历图.html')