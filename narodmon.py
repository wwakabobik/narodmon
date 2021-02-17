from narodmon.interface_api import InterfaceAPI
from narodmon.interface_json import InterfaceJSON


class Narodmon:
    def __init__(self,
                 mac=None, name=None, owner=None, lat=None, lon=None, alt=None,
                 api_key=None, uuid=None, lang=None):
        self.via_json = InterfaceJSON(mac=mac, owner=owner, name=name, lat=lat, lon=lon, alt=alt)
        self.via_api = InterfaceAPI(uuid=uuid, api_key=api_key, lang=lang, lat=lat, lon=lon)
