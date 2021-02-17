from sys import stderr

import requests

from narodmon.tools import status_decode
from narodmon.settings import BASE_API_URL


class InterfaceJSON:
    def __init__(self, mac=None, name=None, owner=None, lat=None, lon=None, alt=None):
        self.endpoint = f'{BASE_API_URL}/json'
        self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        self.name = name
        self.mac = mac
        self.owner = owner
        self.lat = lat
        self.lon = lon
        self.alt = alt

    def set_name(self, name):
        """
        Set/update default name param
        :param name: string
        """
        self.name = name

    def set_mac(self, mac):
        """
        Set/update default mac param
        :param mac: string
        """
        self.mac = mac

    def set_owner(self, owner):
        """
        Set/update default owner param
        :param owner: string
        """
        self.owner = owner

    def set_lat(self, lat):
        """
        Set/update default latitude
        :param lat: latitude (float)
        """
        self.lat = lat

    def set_lon(self, lon):
        """
        Set/update default longitude
        :param lon: longitude (float)
        """
        self.lon = lon

    def set_alt(self, alt):
        """
        Set/update default altitude
        :param alt: altitude (float)
        """
        self.alt = alt

    def send_bulk_data(self, data):
        """
        Send data for several devices

        :param data: list of device data
        :return: response JSON
        """
        if type(data) == list:
            payload = {"devices": data}
            response = requests.post(self.endpoint, json=payload, headers=self.headers)
            status_decode(response)
            return response.json()
        else:
            stderr.write("Narodmon sensors data is wrong!")
            return ''

    def send_full_data(self, sensors, mac=None, name=None, owner=None, lat=None, lon=None, alt=None):
        """
        Send long data (sensors) from device to server

        :param sensors: sensors list or one sensor data (dict)
        :param mac: (optional) mac address of device
        :param name: (optional) name of device
        :param owner: (optional) owner name of device
        :param lat: (optional) latitude (float)
        :param lon: (optional) longitude (float)
        :param alt: (optional) altitude (float)
        :return: response JSON
        """
        payload = {"devices": [self.prepare_device_data_full(sensors=sensors, mac=mac, name=name, owner=owner,
                                                             lat=lat, lon=lon, alt=alt)]}
        response = requests.post(self.endpoint, json=payload, headers=self.headers)
        status_decode(response)
        return response.json()

    def send_short_data(self, sensors, mac=None):
        """
        Send short data (sensors) from device to server

        :param sensors: sensors list or one sensor data (dict)
        :param mac: (optional) mac address of device
        :return: response JSON
        """
        payload = {"devices": [self.prepare_device_data_short(sensors, mac=mac)]}
        response = requests.post(self.endpoint, json=payload, headers=self.headers)
        status_decode(response)
        return response.json()

    def prepare_device_data_full(self, sensors, mac=None, name=None, owner=None, lat=None, lon=None, alt=None):
        """
        Prepare data dict for device (long (create) format)

        :param sensors: sensors list or one sensor data (dict)
        :param mac: (optional) mac address of device
        :param name: (optional) name of device
        :param owner: (optional) owner name of device
        :param lat: (optional) latitude (float)
        :param lon: (optional) longitude (float)
        :param alt: (optional) altitude (float)
        :return: dict with device data
        """
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

    def prepare_device_data_short(self, sensors, mac=None):
        """
        Prepare data dict for device (short (update) format)

        :param sensors: sensors list or one sensor data (dict)
        :param mac: (optional) mac address of device
        :return: dict with device data
        """
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
        Prepare dict of sensor data (for each sensor)

        :param id_in: unique sensor ID (code) (required)
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
            answer.update({"unit": unit})
        if utc_time:
            answer.update({"time": utc_time})
        return answer
