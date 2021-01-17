#!/usr/bin/env python3
"""
htmlreports - A collection of things to help posting
              contest results on the web.

Update History:
* Fri Sep 11 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation
"""
VERSION = '0.0.1' 


           
class HTMLReports():
    def __init__(self, title=None):
        self.doc = self.newdoc()
        if (title):
            self.doc += self.headerstart(title)
        
    def getVersion(self):
       return VERSION
         
    def __version__(self):
       return self.getVersion()
    
    def newdoc(self):
       newdoc = '<!DOCTYPE html>\n'+\
                '<html>\n'
       self.doc = newdoc
       return newdoc
             
    def headerstart(self, docTitle=None, headerStuff = None):
       header = '<head>\n'
       if(docTitle):
           header += '<title>%s</title>\n'%(docTitle)
       if(headerStuff):
           header += '%s\n'%(headerStuff)
           self.doc += header
           header += self.headerend()
       else:
           self.doc += header
       return header 
       
    def headerend(self):
        hend = '</header>\n'
        self.doc += hend
        return hend        

    def bodystart(self, bodyoptions=None, bodytext=None):
       if bodyoptions == None: bodyoptions = ''
       body = '<body %s>\n'%(bodyoptions)
       if (bodytext):
           body += '%s\n'%(bodytext)
           self.doc += body
           body += self.bodyend()
       else:
           self.doc += body
       return body
       
    def bodyend(self):
       bend = '</body>\n'
       self.doc += bend
       return bend
       
    def tabledata(self, data, options=None):
       if options == None: options = ''
       td = '<td %s>%s</td>\n'%(options, data)
       self.doc += td
       return td
       
    def tablerow(self, tdList, options = None):
       if options == None: options = ''
       tr = '<tr %s>\n'%(options)
       self.doc += tr
       for tdl in tdList:
           td = self.tabledata(tdl[0], tdl[1])
           tr += td
       tr += '</tr>\n'
       self.doc += '</tr>\n'
       return tr
              
    def docEnd(self):          
       docend = '</html>\n'
       self.doc += docend
       return docend
       
    def showDoc(self, doc=None):
       if (doc == None):
          doc=self.doc
       print(doc)
       
    def savetoFile(self, pathName, doc=None):
       with open(pathName, 'w') as f:
          if (doc):
              f.write(doc)
          else:
              f.write(self.doc) 
 
if __name__ == '__main__':
   """
   Main - for unit testing new methods
   """   
   app = HTMLReports('This is a test page')
   print ('Classname: %s Version: %s'%(app.__class__.__name__,
                                       app.__version__()))
   #app.headerstart('This is a test page')
   app.headerend() 
   app.bodystart('<h1>Big Main Title</h1>\n<p>This is the main doc</p>\n')  
   app.bodyend()
   app.doc += '<table>\n'
   tabledat = [['R1C1',''],['R1C2',''],['R1C3','']]
   app.tablerow(tabledat,'')
   tabledat = [['R2C1',''],['R2C2',''],['R2C3','']]
   app.tablerow(tabledat,'')
   tabledat = [['R3C1',''],['R3C2',''],['R3C3','']]
   app.tablerow(tabledat,'')
   tabledat = [['R4C1',''],['R4C2',''],['R4C3','']]
   app.tablerow(tabledat,'')
   tabledat = [['R5C1',''],['R5C2',''],['R5C3','']]
   app.tablerow(tabledat,'')
   app.doc+="</table>\n"
   app.bodyend()
   app.docEnd()
   app.showDoc()
