# -*- coding: utf-8 -*-
# @author: xiaoxy
# @time: 2021/9/29 9:17


from docx import Document
from docx.oxml.ns import qn
from docx.shared import Pt, Cm
from docx.enum.text import WD_LINE_SPACING, WD_PARAGRAPH_ALIGNMENT

import config


def generate_file(stock_code, stock_name, price, today):
    document = Document()
    section = document.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    document.styles['Normal'].font.name = u'宋体'
    document.styles['Normal']._element.rPr.rFonts.set(qn('w:eastAsia'), u'宋体')
    document.styles['Normal'].font.size = Pt(14)

    stock_name = stock_name.strip().split(' ')[-1]
    price = sorted(list(set(price)))
    price = '；'.join(str(i) for i in price)

    p1 = document.add_paragraph(
        '		宁波灵均投资管理合伙企业（有限合伙）\n日期：%s\n项目：%s %s\n报价：%s\n\n									操作员：\n									复核员：\n									风控专员：' % (
            today[:4] + '年' + today[4:6] + '月' + today[6:] + '日', stock_code, stock_name, price))
    p_format = p1.paragraph_format
    p_format.line_spacing = 1.5

    document.save(config.output_data_path + today + '/报价单_%s%s.docx' % (stock_code, stock_name))
