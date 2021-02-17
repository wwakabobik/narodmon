import requests

from narodmon.tools import status_decode, generate_hash


class InterfaceAPI:
    def __init__(self, uuid, api_key, lang, lat=None, lon=None):
        self.endpoint = f'{BASE_API_URL}/api'
        self.uuid = uuid,
        self.api_key = api_key
        self.lang = lang
        self.lat = lat
        self.lon = lon

    def prepare_default_payload(self, uuid, api_key, lang, ignore_lang=False):
        if not uuid:
            uuid = self.uuid
        if not api_key:
            api_key = self.api_key
        if not lang:
            lang = self.lang
        payload = {"uuid": uuid, "api_key": api_key}
        if not ignore_lang:
            payload.update({"lang": lang})
        return payload

    def send_post_request(self, payload):
        response = requests.post(url=self.endpoint, json=payload)
        status_decode(response)
        return response.json()

    def app_init(self, lang=None, version=None, platform=None, model=None, width=None, utc=None, api_key=None,
                 uuid=None):
        payload = {"cmd": "appInit"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        payload.update({"api_key": api_key})
        if version:
            payload.update({"version": version})
        if platform:
            payload.update({"platform": platform})
        if model:
            payload.update({"model": model})
        if width:
            payload.update({"width": width})
        if utc:
            payload.update({"utc": utc})

        return self.send_post_request(payload)

    def map_bounds(self, bounds, limit, lang=None, api_key=None, uuid=None):
        payload = {"cmd": "mapBounds"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        payload.update({"bounds": bounds, "limit": limit, "lang": lang})
        return self.send_post_request(payload)

    def sensors_nearby(self, lang=None, lat=None, lon=None, my=None, pub=None, radius=None, limit=None, types=None,
                       trends=None, uuid=None, api_key=None):
        payload = {"cmd": "sensorsNearby"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        if lat:
            payload.update({"lat": lat})
        if lon:
            payload.update({"lon": lon})
        if my:
            payload.update({"my": my})
        if pub:
            payload.update({"pub": pub})
        if radius:
            payload.update({"radius": radius})
        if limit:
            payload.update({"limit": limit})
        if types:
            payload.update({"types": types})
        if trends:
            payload.update({"trends": trends})
        return self.send_post_request(payload)

    def sensors_on_device(self, id_in, trends=None, info=None, api_key=None, uuid=None, lang=None):
        payload = {"cmd": "sensorsOnDevice", "id": id_in}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        if trends:
            payload.update({"trends": trends})
        if info:
            payload.update({"trends": info})
        return self.send_post_request(payload)

    def sensors_values(self, sensors, trends=None, api_key=None, uuid=None):
        payload = {"cmd": "sensorsValues", "sensors": sensors}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        if trends:
            payload.update({"trends": trends})
        return self.send_post_request(payload)

    def sensors_history(self, id_in, period, offset, api_key=None, uuid=None):
        payload = {"cmd": "sensorsHistory", "id": id_in, "period": period, "offset": offset}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def name_sensor(self, id_in, name=None, api_key=None, uuid=None):
        payload = {"cmd": "nameSensor", "id": id_in}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        if name:
            payload.update({"name": name})
        return self.send_post_request(payload)

    def webcams_nearby(self, lat=None, lon=None, limit=None, radius=None, width=None,
                       lang=None, api_key=None, uuid=None):
        payload = {"cmd": "webcamsNearby"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        if lat:
            payload.update({"lat": lat})
        if lon:
            payload.update({"lon": lon})
        if limit:
            payload.update({"limit": limit})
        if radius:
            payload.update({"radius": radius})
        if width:
            payload.update({"width": width})
        return self.send_post_request(payload)

    def webcam_images(self, id_in, limit=None, since=None, latest=None, width=None, uuid=None, api_key=None):
        payload = {"cmd": "webcamImages", "id": id_in}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        if limit:
            payload.update({"limit": limit})
        if since:
            payload.update({"since": since})
        if latest:
            payload.update({"latest": latest})
        if width:
            payload.update({"width": width})
        return self.send_post_request(payload)

    def user_logon(self, login, hash, lang=None, api_key=None, uuid=None):
        payload = {"cmd": "userLogon", "login": login, "hash": hash}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        return self.send_post_request(payload)

    def username(self, api_key=None, uuid=None, lang=None):
        payload = {"cmd": "userLogon"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        return self.send_post_request(payload)['login']

    def register_user(self, login, api_key=None, uuid=None, lang=None):
        payload = {"cmd": "userLogon", "login": login}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        return self.send_post_request(payload)

    def user_location(self, lat=None, lon=None, addr=None, wifi=None, cells=None, gui=None,
                      lang=None, api_key=None, uuid=None):
        payload = {"cmd": "userLocation"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        if lat:
            payload.update({"lat": lat})
        if lon:
            payload.update({"lon": lon})
        if addr:
            payload.update({"addr": addr})
        if wifi:
            payload.update({"wifi": wifi})
        if cells:
            payload.update({"cells": cells})
        if gui:
            payload.update({"gui": gui})
        return self.send_post_request(payload)

    def user_favorites(self, sensors=None, webcams=None, lang=None, api_key=None, uuid=None):
        payload = {"cmd": "userFavorites"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        if type(sensors) == list:
            payload.update({"sensors": sensors})
        if type(webcams):
            payload.update({"webcams": webcams})
        return self.send_post_request(payload)

    def user_logout(self, api_key=None, uuid=None):
        payload = {"cmd": "userLogout"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def add_like(self, id_in, api_key=None, uuid=None):
        payload = {"cmd": "addLike", "id": id_in}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def dis_like(self, id_in, api_key=None, uuid=None):
        payload = {"cmd": "disLike", "id": id_in}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def set_push_token(self, token, api_key=None, uuid=None):
        payload = {"cmd": "setPushToken", "token": token}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def set_push_uri(self, uri, api_key=None, uuid=None):
        payload = {"cmd": "setPushURI", "uri": uri}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def set_push_status(self, states, api_key=None, uuid=None):
        payload = {"cmd": "setPushStatus", "states": states}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def send_command(self, id_in, command, api_key=None, uuid=None):
        payload = {"cmd": "sendCommand", "id": id_in, "command": command}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def send_complaint(self, id_in, problem_time, name, email, problem, value, api_key=None, uuid=None):
        payload = {"cmd": "sendComplaint", "id": id_in, "time": problem_time, "name": name, "email": email,
                   "problem": problem, "value": value}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def send_message(self, subj, mess, uid=None, name=None, chat=None, email=None, images=None,
                     api_key=None, uuid=None):
        payload = {"cmd": "sendMessage", "subj": subj, "mess": mess}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        if type(images) == list:
            payload.update({"images": images})
        if uid:
            payload.update({"uid": uid})
        if name:
            payload.update({"name": name})
        if chat:
            payload.update({"chat": chat})
        if email:
            payload.update({"email": email})
        return self.send_post_request(payload)

    def weather_report(self, lat=None, lon=None, temp=None, humid=None, press=None, wind=None,
                       lang=None, api_key=None, uuid=None):
        if not lat:
            lat = self.lat
        if not lon:
            lon = self.lon
        payload = {"cmd": "weatherReport", "lat": lat, "lon": lon}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        if temp:
            payload.update({"temp": temp})
        if humid:
            payload.update({"humid": humid})
        if press:
            payload.update({"press": press})
        if wind:
            payload.update({"wind": wind})
        return self.send_post_request(payload)

    def bug_report(self, time=None, name=None, email=None, mess=None, logs=None, images=None, api_key=None, uuid=None):
        payload = {"cmd": "bugReport"}
        if time:
            payload.update({"time": time})
        if name:
            payload.update({"email": email})
        if mess:
            payload.update({"mess": mess})
        if logs:
            payload.update({'logs': logs})
        if type(images) == list:
            payload.update({"images": images})
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def get_help(self, topic, lang=None, api_key=None, uuid=None):
        payload = {"cmd": "getHelp"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        if topic:
            payload.update({"topic": topic})
        return self.send_post_request(payload)

    def generate_hash_password(self, password, uuid=None):
        if not uuid:
            uuid = self.uuid
        return f'{generate_hash(uuid)}{generate_hash(password)}'

    def encrypt_uuid(self):
        self.uuid = generate_hash(self.uuid)
