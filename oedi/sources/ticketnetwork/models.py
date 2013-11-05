from ..models import Performer as BasePerformer
from ..models import Event as BaseEvent
from ..models import Venue as BaseVenue

from ... import models


class Performer(BasePerformer):
    provider_id = 1
    source_id = "ticketnetwork"
    name_field = "PerformerName"

    def normalize(self):
        return models.Performer(**{
            "name": self.data.get("PerformerName", ""),
            "categories": [self.data.get("ParentCategory"),
                           self.data.get("ChildCategory"),
                           self.data.get("GrandChildCategory")]

        })


class Event(BaseEvent):
    provider_id = 1
    source_id = "ticketnetwork"


class Venue(BaseVenue):
    provider_id = 1
    source_id = "ticketnetwork"

    name_field = "venuename"
    street_field = "venuestreet1"
    zip_field = "venuestreet2"
    state_field = "venuestateprovince"

    def normalize(self):
        return models.Venue(self.source_id, **{
            "name": self.data.get("venuename", ""),
            "url": self.data.get("venueurl", ""),
            "directions": self.data.get("venuedirections", ""),
            "rules": self.data.get("venuerules", ""),
            "street1": self.data.get("venuestreet1", ""),
            "street2": self.data.get("venuestreet2", ""),
            "stateprovince": self.data.get("venuestateprovince", ""),
            "zip": self.data.get("venuezip", ""),
            "country": self.data.get("venuestatecountry", ""),
        })