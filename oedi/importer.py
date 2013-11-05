from multiprocessing import Process
from cement.core import controller

from .sources.ticketnetwork.importers import PerformerImporter, EventImporter, VenueImporter


class Importer(controller.CementBaseController):
    class Meta:
        label = "importer"

    @controller.expose(hide=False)
    def ticketnetwork(self):
        args = {
            "csv_path": "/Users/chris/tmp/",
            "es_hosts": ["http://localhost:9200"]
        }

        processes = [Process(target=PerformerImporter(**args)),
                     Process(target=EventImporter(**args)),
                     Process(target=VenueImporter(**args))]

        print "Starting processes"
        for process in processes:
            process.start()

        print "Joining processes"
        for process in processes:
            process.join()

    @controller.expose(hide=False)
    def performers(self):
        PerformerImporter(csv_path="/Users/chris/tmp/", es_hosts=["http://localhost:9200"])()
