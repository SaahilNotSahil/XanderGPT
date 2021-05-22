import mongoengine


class Link(mongoengine.Document):
    _branch = mongoengine.StringField()
    _ph = mongoengine.URLField()
    _cy = mongoengine.URLField()
    _ss = mongoengine.URLField()
