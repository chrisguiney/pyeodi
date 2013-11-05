import hashlib
import arrow


class Source(object):

    provider_id = None
    source_id = None
    data_id = None
    name_field = None

    def __init__(self, data):
        self.data = data
        self.created = arrow.utcnow()
        self.updated = arrow.utcnow()

    def dict(self):
        return {
            "providerId": self.provider_id,
            "sourceId": self.source_id,
            "dataId": self.data_id,
            "data": self.data,
            "created": self.created.timestamp * 1000,
            "updated": self.updated.timestamp * 1000
        }

    def hash(self):
        values = [v.encode('utf-8').strip().lower() if isinstance(v, basestring) else str(v)
                  for v in filter(None, self.data.itervalues())]
        return hashlib.md5(''.join(values)).hexdigest()

    def normalize(self):
        raise NotImplementedError


class Performer(Source):
    data_id = "performer"


class Event(Source):
    data_id = "event"


class Venue(Source):
    data_id = "venue"
    street_field = None
    zip_field = None
    state_field = None

    def hash(self):
        values = [v.encode('utf-8').strip().lower()
                  for v in filter(None, (self.data.get(self.name_field),
                                         self.data.get(self.street_field),
                                         self.data.get(self.state_field),
                                         self.data.get(self.zip_field)))]
        return hashlib.md5(''.join(values)).hexdigest()