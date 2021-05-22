import mongoengine


class Link(mongoengine.Document):
    _courses = mongoengine.DictField()
