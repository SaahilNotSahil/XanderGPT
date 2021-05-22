import mongoengine


class Link(mongoengine.Document):
    _branch = mongoengine.StringField()
    _ph = mongoengine.URLField(default='https://classroom.google.com')
    _cy = mongoengine.URLField(default='https://classroom.google.com/')
    _ss = mongoengine.URLField(default='https://classroom.google.com')
