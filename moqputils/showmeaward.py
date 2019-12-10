#!/usr/bin/python
"""
ShowMe  - Determine which Missouri QSO Party stations 
          qualify for the ShowMe and/or MISSOURI awards

Update History:
* Thu Dec 09 2019 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - Start of work
"""

COMMONCALLS = ['K0M', 'N0M','W0M',
               'K0O', 'N0O','W0O',
               'K0S', 'N0S','W0S']
               
SHOWMECALLS = ['K0H', 'N0H','W0H',
               'K0W', 'N0W','W0W',
               'K0E', 'N0E','W0E']
                
MISSOURICALLS = ['K0I', 'N0I','W0I',
                 'K0U', 'N0U','W0U',
                 'K0R', 'N0R','W0R']


SHOWMEKEYS = 'SHOWME'

MOKEYS = 'MISSOURI'

class ShowMeAward():
    award = dict()
    award = {'S':None,
    'H':None,
    'O':None,
    'W':None,
    'M':None,
    'E':None}

    def __init__(self, filename=None):
        if (filename):
           if (filename):
              self.appMain(filename)

    def _bingo_(self, award, KEYS):
        bingo = True
        for key in KEYS:
            if (award[key] == None):
               bingo = False
               break
        return bingo
    
    def _checkcall_(self, call):
       #print(call)
       if ( (call in COMMONCALLS) or \
            (call in SHOWMECALLS) ):
          key = call[2] 
          #print('call = %s, key = %s'%(call, key))
          if (key in self.award):
              #print('Found %s for key %s'%(call, key))
              if (self.award[key] == None):
                  self.award[key] = call

    def checkLog(self, logqsos):
       showme = False
       for qso in logqsos:
          self._checkcall_(qso['URCALL'])
          if (self._bingo_(self.award, SHOWMEKEYS)):
              print('***BINGO*** - SHOWME complete!')
              Showme = True
              print(award)
              break
          else:
              print('Not Bingo!')
          #print(qso)
          #print(self.award)
       return showme
       
    def appMain(self, pathname):
        print(self.checkLog(pathname))
        print(self.award)      

if __name__ == '__main__':
   app = ShowMeAward()
   """
   app._checkcall_('N0S')
   app._checkcall_('W0H')
   app._checkcall_('W0O')
   app._checkcall_('W0W')
   app._checkcall_('W0M')
   app._checkcall_('W0E')
   print(app._bingo_(app.award, SHOWMEKEYS))
   print(app.award)
   """
