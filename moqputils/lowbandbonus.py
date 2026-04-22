#!/usr/bin/env python3
"""
lowBandBonus  - Computes bonus points for the Low Band Early Day
                QSO bonus added by the 2026 rules.

Update History:
* Tue Apr 21 2026 Mike Heitmann, N0SO <n0so@arrl.net>
- V0.0.1 - First interation
"""

querystg = """
SELECT FREQ, DATETIME, LOGID, VALID
FROM QSOS
WHERE
(VALID=1 AND LOGID={})
AND
(
(FREQ BETWEEN 7000 AND 7300)
OR
(FREQ BETWEEN 3500 AND 4000)
)
AND
(
(DATETIME BETWEEN '{}' AND '{}')
OR
(DATETIME BETWEEN '{}' AND '{}')
)
ORDER BY DATETIME
           """
MAXBONUS=250 # For 2026
DAY1B = '2026-04-11 14:00:00'
DAY1E = '2026-04-11 20:00:00' 
DAY2B = '2026-04-12 14:00:00'
DAY2E = '2026-04-12 20:00:00' 

VERSION = '0.0.1'

class lowBandBonus():
    def __init__(self,  callsign=None,
                        db=None):
        self.callsign = callsign
        self.db = db
        self.qsoCount = 0
        self.bonus = 0
        self.lid = 0
        
        if callsign and db:
            res = self.compute_bonus(self.callsign, self.db)
            #print(f'{res=}')
        pass
        
    def getBonus(self, asdict=False):
        if asdict:
            return {"CALLSIGN": self.callsign,
                    "LOGID": self.lid,
                    "BONUS": self.bonus,
                    "QCOUNT": self.qsoCount}
        else:
            return [self.callsign, self.lid, self.qsoCount, self.bonus]
        

    def compute_bonus(self, call, db):
        lid=0
        bonus=0
        qsocount=0
        if type(call) is str:
            # Get logid from database
            _t = db.CallinLogDB(call)
            if _t:
                lid=_t
            else:
                print(f'lowBandBonus: {call=} : Not found in the database!')
        elif type(call) is int:
            lid=call
        else:
            print(f'lowBandBonus: {call=} : Not a callsign or log id!')
        
        if lid > 0:
            #qs = querystg.format(lid, DAY1B, DAY1E, DAY2B, DAY2E)
            #print(f'{qs=}')
            qsos = db.read_query(querystg.format(lid, DAY1B, DAY1E,
                                                 DAY2B, DAY2E))
            if qsos:
                qsocount=len(qsos)
                if qsocount > 0:
                    if qsocount <= MAXBONUS:
                        bonus = qsocount
                    else:
                        bonus = MAXBONUS
        self.qsoCount = qsocount
        self.bonus = bonus
        self.lid = lid
        return self.getBonus()

 
