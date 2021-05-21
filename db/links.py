import mongoengine
import datetime


class Link(mongoengine.Document):
    _branch = mongoengine.StringField()
    _reg_date = mongoengine.DateTimeField(default=datetime.datetime.now())
