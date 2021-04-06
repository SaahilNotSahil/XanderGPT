import mongoengine
import datetime

class Link(mongoengine.Document):
    _branch = mongoengine.StringField()
    ics = mongoengine.URLField()
    em = mongoengine.URLField()
    emtut = mongoengine.URLField()
    maths = mongoengine.URLField()
    mathstut = mongoengine.URLField()
    icslab1 = mongoengine.URLField()
    icslab2 = mongoengine.URLField()
    icslab3 = mongoengine.URLField()
    _reg_date = mongoengine.DateTimeField(default=datetime.datetime.now())
    
    links = {
        "ics": ics,
        "em": em,
        "emtut": emtut,
        "maths": maths,
        "mathstut": mathstut,
        "icslab1": icslab1,
        "icslab2": icslab2,
        "icslab3": icslab3
    }
    