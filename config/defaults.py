import datetime as dt

# Initial Date for Seasons model
SEASONS = [{'name':'Summer', 'start':dt.date(1976,6,22), 'end':dt.date(1976,9,21),
             'color':"#FF3300"},
           {'name':'Fall', 'start':dt.date(1976,9,22), 'end':dt.date(1976,12,21),
            'color':"#CC6600"},
           {'name':'Winter', 'start':dt.date(1976,12,22), 'end':dt.date(1976,3,21),
            'color':"#CCFFFF"},
           {'name':'Spring', 'start':dt.date(1976,3,22), 'end':dt.date(1976,6,21),
            'color':"#66FF33"},]

def load_seasons():
    from seasons.models import Season as model
    for s in SEASONS:
        new_entry = model(**s)
        new_entry.save()



