#!/usr/bin/env python3

import datetime
from webbrowser import open_new_tab
from htmlutils.htmltable import *

class htmlDoc():
    def __init__(self, document = None):
        if (document):
            self.document = document
        else:
            self.document = self.newDoc()
            
    def newDoc(self, existingDoc = None):
        if(existingDoc):
            self.document = existingDoc
        else:
            self.document = '<html>\n'
            
        return self.document

    def closeDoc(self, document = None):
        ctext = '</html>\n'
        retVal = self.add_unformated_text(ctext, document)
        return retVal

    def openHead(self, title,
                           stylelink = None,
                           document = None):
        retVal = None
        htext = '<head>\n<title>%s</title>\n'%title
        if (stylelink):
            htext += """<link href="%s" rel="stylesheet" type="text/css" />\n"""%stylelink
        if (document):
            retVal = document + htext
        else:
            retVal = htext
            self.document += htext
        return retVal
            
    def closeHead(self, document = None):
        ctext = '</head>\n'
        retVal = self.add_unformated_text(ctext, document)
        return retVal

    def openBody(self, document=None):
        ctext = '<body>\n'
        retVal = self.add_unformated_text(ctext, document)
        return retVal

    def closeBody(self, document=None):
        ctext = '</body>\n'
        retVal = self.add_unformated_text(ctext, document)
        return retVal

    def get_Doc(self):
        return self.document

    def showDoc(self, document = None):
        if (document):
            displayDco = document
        else:
            displayDoc = self.document
        print(displayDoc)
        
    def add_unformated_text(self, text, document=None):
        retVal = None
        if (document):
            document += text
            retVal = document
        else:
            self.document += text
            retVal = text
        return retVal
    
    def addTable(self, tdata, header=False,
                 caption = None,
                 document=None):
        t = htmlTable()
        retVal = self.add_unformated_text(\
            t.makeTable(tdata,
                        header,
                        caption), document)
        return retVal
           
    def addTablefromDict(self, dictList,
                               HeaderList = None,
                               caption = None,
                               dictIndexList = None,
                               document = None):
       if (dictIndexList): 
           pass
       else:
           dictIndexList = dictList[0].keys()
       tableList =[]
       if (HeaderList):
           tableList.append(HeaderList)

       for station in dictList:
           row = []
           for key in dictIndexList:
               row.append(  '%s' % (station[key]))
           tableList.append(row)
       retVal = self.addTable(tableList, 
                              HeaderList,
                              caption,
                              document)
       return retVal
            
    def saveasFile(self, filename, document = None):
        if (document):
            with open(filename,'w') as f:
                f.writelines(document)
                f.close()
        else:
            with open(filename,'w') as f:
                f.writelines(self.document)
                f.close()

    def saveAndView(self, filename, document = None):
        self.saveasFile(filename, document)
        open_new_tab(filename)
        
    def addTimeTag(self, 
                    prefix=None, 
                    tagType=None, 
                    document=None):
        now = datetime.datetime.utcnow().strftime("%Y%m%d-%H%M%S")
        if (prefix==None): prefix=''
        if (tagType):
            tagType=tagType.lower()
            if(tagType=='comment'):
                fmtstg='<!-- %s%s UTC -->\n'
        else:
            fmtstg='<p>%s %s UTC</p>\n'
        ctext = fmtstg % (prefix, now)
        retVal = self.add_unformated_text(ctext, document)
        return retVal

