import mongoengine
import datetime


class Link(mongoengine.Document):
    _branch = mongoengine.StringField()

    ics = mongoengine.StringField()
    ee = mongoengine.StringField()
    bio = mongoengine.StringField()
    em = mongoengine.StringField()
    emtut = mongoengine.DictField()
    maths = mongoengine.ListField()
    mathstut = mongoengine.DictField()
    icslab = mongoengine.DictField()
    eelab = mongoengine.DictField()

    _reg_date = mongoengine.DateTimeField(default=datetime.datetime.now())
