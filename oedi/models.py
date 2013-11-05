def merge_iterable(a, b):
    if isinstance(a, set) or isinstance(b, set):
        return set().union(set(a), set(b))
    else:
        return a + b


class Model(object):
    field_list = ()

    def __init__(self, source, **kwargs):
        self.source = source

        if isinstance(source, list):
            self.source = set(source)
        elif not isinstance(source, set):
            self.source = {source}

        for key in kwargs.keys():
            if key not in self.field_list:
                raise ValueError("%s is not a valid field" % key)

        self.doc = kwargs

    #Dynamically accessible items from doc
    def __getattr__(self, item):
        if item in self.field_list:
            return self.doc.get(item)
        return super(Model, self).__getattribute__(item)

    def __setattr__(self, key, value):
        if key in self.field_list:
            self.doc[key] = value
            return
        super(Model, self).__setattr__(key, value)

    #Merge functionality
    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Models must be of the same type to be merged")
        new_doc = {}
        new_doc.update(other.doc)

        for key, val in self.doc.iteritems():
            if isinstance(val, (list, tuple, set)) and key in new_doc:
                new_doc[key] = merge_iterable(new_doc[key], val)
            else:
                new_doc[key] = val

        return self.__class__(set().union(self.source, other.source), **new_doc)

    def __radd__(self, other):
        #Sum starts out with 0
        if not isinstance(other, self.__class__):
            return self
        return other.__add__(self)


class Performer(Model):
    field_list = ("name", "categories")


class Venue(Model):
    field_list = ("name",
                  "url",
                  "directions",
                  "rules",
                  "street1",
                  "street2",
                  "stateprovince",
                  "zip",
                  "country")


class Event(Model):
    pass
