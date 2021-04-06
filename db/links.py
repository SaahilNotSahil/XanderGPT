import mongoengine
import datetime

class Link(mongoengine.Document):
    _branch = mongoengine.StringField()
    ics = mongoengine.StringField()
    em = mongoengine.StringField()
    emtut = mongoengine.StringField()
    maths = mongoengine.StringField()
    mathstut = mongoengine.StringField()
    icslab1 = mongoengine.StringField()
    icslab2 = mongoengine.StringField()
    icslab3 = mongoengine.StringField()
    _reg_date = mongoengine.DateTimeField(default=datetime.datetime.now())
    
    courses = [ics, em, emtut, maths, mathstut, icslab1, icslab2, icslab3]
    