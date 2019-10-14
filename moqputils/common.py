class common():
    def __init__(self):
        pass
        
    def __get_app_version__(self):
        from __init__ import VERSION
        versions = 'csv2cab V'+VERSION+'\n' 
        from csv2cab import csv2CAB
        TEMP = csv2CAB()
        versions+='csv2CAB V'+TEMP.__version__()+'\n'
        from CabrilloUtils import CabrilloUtils
        TEMP = CabrilloUtils()
        versions+='CabrilloUtils V'+TEMP.getVersion()+'\n'
        from ui import gui_csv2cab
        TEMP = gui_csv2cab(RUN=False)
        versions+='ui V'+TEMP.__version__()+'\n'
        return versions
