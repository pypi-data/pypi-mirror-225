#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @IDE       :PyCharm
# @FileName  :evolvement.py
# @Time      :2023/8/2 17:18
# @Author    :Darius

from docx.shared import Pt
from docx.oxml.ns import qn

# 白名单
__all__ = [
    "alter_table"
]


def alter_table(txt: str, paragraphs_num: int, table=None, cell: tuple | list = (0, 1),
                size: str | float | int = "四号", english_font: str = "Times New Roman", font: str = "仿宋_GB2312",
                underline: bool = False, clear: bool = True):
    """
    修改指定表格位置内容（主要针对GA调证）
    :param txt: 修改文本
    :param table: 表，需要传入定位后的表
    :param paragraphs_num: 定位段落
    :param cell: 定位单元格（只获取索引0、1，多传无效），默认为 (0, 1)
    :param size: 字体大小（与word字体名称对应）
    :param english_font: 英文字体样式，默认为 "Times New Roman"（与word字体样式名称对应）
    :param font: 字体样式，默认为 ”仿宋_GB2312“（与word字体样式名称对应）
    :param underline: 下划线开关
    :param clear: 删除原字符，默认为 True
    :return:
    """
    size_relation = {
        "初号": 44,
        "小初": 36,
        "一号": 26,
        "小一": 24,
        "二号": 22,
        "小二": 18,
        "三号": 16,
        "小三": 15,
        "四号": 14,
        "小四": 12,
        "五号": 10.5,
        "小五": 9,
        "六号": 7.5,
        "小六": 6.5,
        "七号": 5.5,
        "八号": 5
    }
    if type(size) == str:
        size = size_relation[size]
    if table is not None:
        cell = table.cell(cell[0], cell[1])  # 定位单元格
    paragraph = cell.paragraphs[paragraphs_num]  # 定位段落
    if clear:
        paragraph.clear()  # 删除原字符
    paragraph_txt = paragraph.add_run(txt)  # 添加新字符
    paragraph_txt.font.size = Pt(size)  # 字体大小（磅）
    paragraph_txt.font.name = english_font  # 英文字体
    paragraph_txt.element.rPr.rFonts.set(qn('w:eastAsia'), font)  # 中文字体
    paragraph_txt.underline = underline  # 下划线
