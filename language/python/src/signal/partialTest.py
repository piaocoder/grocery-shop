from functools import partial
from datetime import datetime,timedelta  

def GetNextDay(baseday,n):  
    return str((datetime.strptime(str(baseday),
        '%Y-%m-%d')+timedelta(days=n)).date())  


nday = partial(GetNextDay, '2015-01-01')
print nday(1)
print nday(3)
