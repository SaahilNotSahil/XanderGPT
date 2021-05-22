import mongoengine


class Link(mongoengine.Document):
    _branch = mongoengine.StringField()
    _ph = mongoengine.URLField(default='')
    _cy = mongoengine.URLField(default='')
    _ss = mongoengine.URLField(default='')
