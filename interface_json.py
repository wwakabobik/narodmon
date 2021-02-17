from sys import stderr

import requests

from narodmon.tools import status_decode


class InterfaceJSON:
    def __init__(self, mac=None, name=None, owner=None, lat=None, lon=None, alt=None):
        self.endpoint = f'{BASE_API_URL}/json'
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.name = name,
        self.mac = mac
        self.owner = owner
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def set_name(self, name):
        self.name = name

    def set_mac(self, mac):
        self.mac = mac

    def set_owner(self, owner):
        self.owner = owner

    def set_lat(self, lat):
        self.lat = lat

    def set_lon(self, lon):
        self.lon = lon

    def set_alt(self, alt):
        self.alt = alt

    def send_several_data_json(self, data):
        if type(data) == list:
            payload = {"devices": data}
            response = requests.post(self.endpoint, json=payload, headers=self.headers)
            status_decode(response)
            return response.json()
        else:
            stderr.write("Narodmon sensors data is wrong!")
            return ''

    def send_full_data_json(self, sensors, mac=None, name=None, owner=None, lat=None, lon=None, alt=None):
        payload = {"devices": [self.prepare_device_data_full(sensors=sensors, mac=mac, name=name, owner=owner,
                                                             lat=lat, lon=lon, alt=alt)]}
        response = requests.post(self.endpoint, json=payload, headers=self.headers)
        self.status_decode(response)
        return response.json()

    def send_short_data_json(self, sensors, mac=None):
        payload = {"devices": [self.prepare_data_short(sensors, mac=mac)]}
        response = requests.post(self.endpoint, json=payload, headers=self.headers)
        status_decode(response)
        return response.json()

    def prepare_device_data_full(self, sensors, mac=None, name=None, owner=None, lat=None, lon=None, alt=None):
        if type(sensors) == dict:
            sensors = [sensors]
        elif type(sensors) == list:
            pass
        else:
            stderr.write("Narodmon sensors data is wrong!")
            return ''

        if not mac:
            mac = self.mac
        if not name:
            name = self.name
        if not owner:
            owner = self.owner
        if not lat:
            lat = self.lat
        if not lon:
            lon = self.lon
        if not alt:
            alt = self.alt

        return {"mac": mac, "name": name, "owner": owner, "lat": lat, "lon": lon, "alt": alt, "sensors": sensors}

    def prepare_data_short(self, sensors, mac=None):
        if type(sensors) == dict:
            sensors = [sensors]
        elif type(sensors) == list:
            pass
        else:
            stderr.write("Narodmon sensors data is wrong!")
            return ''

        if not mac:
            mac = self.mac

        return {"devices": [{"mac": mac, "sensors": sensors}]}

    @staticmethod
    def prepare_sensor_data(id_in, value, name=None, unit=None, utc_time=None):
        """
        :param id: unique sensor ID (code) (required)
        :param value: sensor value (float) (required)
        :param name: public name of sensor (string) (optional)
        :param unit: unit (string) (optional)
        :param utc_time: utc timestamp (long int) (optional if measurements for now)
        :return: dict with sensor data
        """
        answer = {"id": id_in, "value": value}
        if name:
            answer.update({"name": name})
        if unit:
            answer.update({"unit": "C"})
        if utc_time:
            answer.update({"time": utc_time})
        return answer
