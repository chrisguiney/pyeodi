import os
from csv import DictReader
from functools import partial

from pyes import ES

from .models import Performer, Event, Venue


def sanitize(entry):
    for k, v in entry.iteritems():
        if isinstance(v, basestring):
            entry[k] = v.decode("ISO-8859-1")


class Importer(object):
    base_filename = "TicketNetworkDataFeed"

    model_map = {
        "performers": {
            "file": "Performers.csv",
            "model": Performer,
        },
        "events": {
            "file": "Events.csv",
            "model": Event,
        },
        "venues": {
            "file": "Venues.csv",
            "model": Venue,
        }
    }

    def __init__(self, data_type, csv_path="/tmp/", es_hosts=("http://localhost:9200",)):
        self.data_type = data_type
        self.doc_type = "ticketnetwork_%s" % self.data_type
        self.csv_path = csv_path
        self.es = ES(es_hosts)

    def model(self):
        return self.model_map[self.data_type]["model"]

    def filepath(self):
        return os.path.join(self.csv_path,
                            '-'.join([self.base_filename, self.model_map[self.data_type]["file"]]))

    def __call__(self, *args, **kwargs):
        with open(self.filepath()) as f:
            reader = DictReader(f)
            for entry in reader:
                sanitize(entry)
                model = self.model()(entry)
                d = model.dict()
                self.es.index(d, "oedi_sources", self.doc_type, model.hash(), bulk=True)
            self.es.flush_bulk(True)

PerformerImporter = partial(Importer, "performers")
EventImporter = partial(Importer, "events")
VenueImporter = partial(Importer, "venues")