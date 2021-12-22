#!/usr/bin/env python3
from htmlutils.htmltable import *
from htmlutils.htmldoc import *

doc = ''

tableData = [('H1','H2','H3','H4','H5','H6','H7','H8'),
             ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8'),
             ('B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8'),
             ('C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8')]
             
T = htmlTable()

td = T.makeTable(tableData,
                 header=True,
                 caption='This is my Caption')


d = htmlDoc()
d.openHead('This is a test...',
                     './styles.css')

d.closeHead()
d.openBody()
d.addTimeTag(prefix='Report Generated On ', tagType='comment')
d.addTable(tableData, header=True,
                 caption='Table inhtmlDoc')
d.closeBody()
d.closeDoc()

d.showDoc()
d.saveAndView('ttest1.html')
