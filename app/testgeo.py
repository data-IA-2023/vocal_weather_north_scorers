from geopy.geocoders import Nominatim
from transformers import pipeline

def city_to_coordinates(city):
    geolocator = Nominatim(user_agent="vocal_weather_app")
    location = geolocator.geocode(city)
    lat = location.latitude
    lon = location.longitude
    return({'lat': lat,
            'lon' : lon})

def prep_bert():
    nlp = pipeline("ner", model = "saved_pipe")
    return nlp

def localisation_func(a,b):
    a=a.lower()
    a=virgule(a)
    a=a.split(' ')
    b=underscore(b)
    c=[]
    for i in range(len(a)):
        if a[i] in b:
            if i!=0 and a[i-1] in b:
                c[-1]=c[-1]+' '+a[i]
            else:
                c.append(a[i])
    return c

def create_entity(a,nlp):
    doc = nlp(a)
    loc=[i['word'] for i in doc if i['entity'] in ['I-LOC']]
    dat=[i['word'] for i in doc if i['entity'] in ['I-DATE']]  
    return({'loc': loc,
            'dat' : dat})

def colle_mot(a):
    b=[]
    for i in a:
        if len(i)==1 and i[0]=='h':
            i=':'
        if i[0]!='▁' and len(b)!=0:
            b[-1]+=i
        else:
            b.append(i)
    return b

def virgule(a):
    b=""
    a = a.lower().replace('\xa0', '')
    for carac in a:
        if carac==',' or carac== ';' or carac== '.' or carac== '?' or carac== '!':
            b+=' , '
        else:
            b+=carac
    return b

def underscore(a):
    a=' '.join(a)
    b=''
    for carac in a:
        if carac=='▁':
            b+=''
        else:
            b+=carac
    b=b.lower()
    b=b.split(' ')
    return b

def test_coord():   
    nlp = prep_bert()
    text_donne = "Je veux la météo à Paris"
    entites=create_entity(text_donne,nlp)

    if len(entites['loc'])==0:
        error_message="Veuillez donner une localisation précise"
        
    loc=colle_mot(entites['loc'])
    loc=localisation_func(text_donne,loc)
    if len(entites['dat'])==0:
            heure_actuelle = datetime.now().replace(minute=0, second=0, microsecond=0)
            heure_actu = heure_actuelle.strftime("%Hh00")
            date_base=f"aujourd'hui à {heure_actu}"
            entites['dat'].append(date_base)
    dat=colle_mot(entites['dat'])
    dat=underscore(dat)
    dat=' '.join(dat)
    date_final=date(dat)

    monitoring['date']=date_final
    monitoring['localisations']=[]
    monitoring['coord']={}
    monitoring['status_code_geoloc']={}
    monitoring['status_code_weather']={}
    monitoring['dico_meteo']={}

    for localisation in loc:
        monitoring['localisations'].append(localisation)
        coord,status_code_geoloc=city_to_coordinates(localisation)
        monitoring['coord'][localisation]=coord
        monitoring['status_code_geoloc'][localisation]=status_code_geoloc