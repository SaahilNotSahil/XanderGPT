import mongoengine


class Link(mongoengine.Document):
    _courses = {
        'ph': {
            'branches': [],
            'links': []
        },
        'cy': {
            'branches': [],
            'links': []
        },
        'ss': {
            'branches': [],
            'links': []
        }
    }
