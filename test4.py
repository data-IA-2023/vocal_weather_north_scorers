def colle_mot(a):
    b=[]
    for i in a:
        if len(i)==1 and i[0]=='h':
            i=':'
        if i[0]!='_':
            b[-1]+=i
        else:
            b.append(i)
    return b
            
print(colle_mot(['_bon','_j','our','_je','_suis','h','_un','_h','omm','e']))

import re
from datetime import datetime, timedelta
def date(a):
    jours=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    date = r'(aujourd\'hui|demain|aprèsmain|après-demain|dans (\d+) h|lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|(\d+) jour)'
    time = r'(matin|après-midi|soir|nuit|\d+:\d+)(?:\s*(?:à|jusqu\'à)\s*(\d+:\d+))?'
    b=re.search(date, a)
    c=re.search(time,a)
    time1=datetime.now().date()
    if b:
        hour=True
        if b.group(1)=="aujourd'hui":
            time1=time1
        elif b.group(1)=="demain":
            time1=time1+timedelta(days=1)
        elif b.group(1)=="lundi":
            jour='monday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="mardi":
            jour='tuesday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="mercredi":
            jour='wednesday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="jeudi":
            jour='thursday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="vendredi":
            jour='friday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="samedi":
            jour='saturday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=="dimanche":
            jour='sunday'
            jour_actuel=time1.strftime("%A").lower()
            difference=(7 + (jours.index(jour) - jours.index(jour_actuel))) % 7
            time1=time1+timedelta(days=difference)
        elif b.group(1)=='après-demain' or b.group(1)=='aprèsmain':
            time1=time1+timedelta(days=2)
        elif b.group(2) and 'h' not in a:
            time1=time1+timedelta(days=int(b.group(2)))
        elif b.group(1) and 'h' in a:
            time2=(datetime.now())+timedelta(hours=int(b.group(2)))
            time1 = time2.date()
            base_time = time2.strftime("%H:%M:%S")
            interval=False
            hour=False
    else:
        time1=time1
    if c:
        if c.group(1)=='matin':
            base_time='06:00:00'
            interval=False
        elif c.group(1)=='après-midi':
            base_time='13:00:00'
            interval=False
        elif c.group(1)=='soir':
            base_time='18:00:00'
            interval=False
        elif c.group(1)=='nuit':
            base_time='24:00:00'
            interval=False
        elif c.group(1)=='midi':
            base_time='10:00:00'
            interval=False
        else :
            base_time=c.group(1)+':00'
            interval=False
            if c.group(2):
                 base_time2=c.group(2)+':00'
                 interval=True
    elif hour==True:
        base_time='12:00:00'
        interval=False
    time_final = datetime.combine(time1, datetime.strptime(base_time, '%H:%M:%S').time())
    if interval==False:
        time_final2=time_final+timedelta(hours=5)
    else:
        time_final2=datetime.combine(time1, datetime.strptime(base_time2, '%H:%M:%S').time())
    d=[]
    while time_final2>time_final:
        d.append(time_final.strftime('%Y-%m-%d %H:%M:%S'))
        time_final=time_final+timedelta(hours=1)
    return d

print(date(' dans 5 h'))



    
