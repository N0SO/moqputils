#!/usr/bin/env python3
class htmlTable():

    def __init__(self, document = None):
        if (document):
            self.document = document
        else:
            self.document = ""
           
           
    def makeCell(self, cdata, header=False):
        if(header):
            fmt = """<th>%s</th>"""
        else:
            fmt = """<td>%s</td>"""           
        return fmt % (cdata)

    def makeRow(self, rowData, header=False):
        row = ""
        for celldata in rowData:
            row += self.makeCell(celldata, header)
        return '<tr>%s</tr>' % row 
        

    def makeTable(self, tdata, header=None, caption=None,):
       retData = '<p><table>\n'
       if (caption):
            retData += '<caption>%s</caption>\n' % caption
       if (header):
            firstLine = True
       else:
            firstLine = False
       rowCount = 0
       for row in tdata:
            retData += '%s\n'%self.makeRow(row, firstLine)
            firstLine = False
            rowCount+=1
       retData += '</table></p>\n'

       return retData
