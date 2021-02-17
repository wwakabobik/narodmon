import string
import random

from hamcrest import assert_that, only_contains, contains
import pytest

from narodmon import Narodmon


def random_string(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


@pytest.fixture
def nm_initialized():
    rmac = random_string(random.randint(1, 20))
    rowner = random_string(random.randint(1, 20))
    rname = random_string(random.randint(1, 20))
    rlon = random.uniform(-180, 180)
    rlat = random.uniform(90, 90)
    ralt = random.uniform(-4000, 9000)
    nm = Narodmon(mac=rmac, lat=rlat, lon=rlon, alt=ralt, owner=rowner, name=rname)
    return nm


@pytest.fixture
def sensor_data():
    nm = Narodmon()

    def func():
        rid = random_string(random.randint(1, 20))
        rval = random.uniform(-999999, 999999)
        runit = random_string(random.randint(1, 3))
        rutc = random.randint(0, 999999999)
        response = nm.via_json.prepare_sensor_data(id_in=rid, value=rval, unit=runit, utc_time=rutc)
        return response

    return func


def test_json_empty_init():
    nm = Narodmon()
    assert_that(
        (
            nm.via_json.mac,
            nm.via_json.lon,
            nm.via_json.lat,
            nm.via_json.alt,
            nm.via_json.owner,
            nm.via_json.name
        )
    ), only_contains(None)


def test_json_set_mac():
    nm = Narodmon()
    rstring = random_string(random.randint(1, 20))
    nm.via_json.set_mac(rstring)
    assert nm.via_json.mac == rstring


def test_json_set_lat():
    nm = Narodmon()
    random_number = random.uniform(-90, 90)
    nm.via_json.set_lat(random_number)
    assert nm.via_json.lat == random_number


def test_json_set_lon():
    nm = Narodmon()
    random_number = random.uniform(-180, 180)
    nm.via_json.set_lon(random_number)
    assert nm.via_json.lon == random_number


def test_json_set_alt():
    nm = Narodmon()
    random_number = random.uniform(-4000, 9000)
    nm.via_json.set_alt(random_number)
    assert nm.via_json.alt == random_number


def test_json_set_owner():
    nm = Narodmon()
    rstring = random_string(random.randint(1, 20))
    nm.via_json.set_owner(rstring)
    assert nm.via_json.owner == rstring


def test_json_set_name():
    nm = Narodmon()
    rstring = random_string(random.randint(1, 20))
    nm.via_json.set_name(rstring)
    assert nm.via_json.name == rstring


def test_json_default_init():
    rmac = random_string(random.randint(1, 20))
    rowner = random_string(random.randint(1, 20))
    rname = random_string(random.randint(1, 20))
    rlon = random.uniform(-180, 180)
    rlat = random.uniform(90, 90)
    ralt = random.uniform(-4000, 9000)

    nm = Narodmon(mac=rmac, lat=rlat, lon=rlon, alt=ralt, owner=rowner, name=rname)
    assert_that(
        (
            nm.via_json.mac,
            nm.via_json.lon,
            nm.via_json.lat,
            nm.via_json.alt,
            nm.via_json.owner,
            nm.via_json.name
        )
    ), contains(rmac, rlon, rlat, ralt, rowner, rname)


def test_json_prepare_sensor_data_default(nm_initialized):
    nm = nm_initialized
    rid = random_string(random.randint(1, 20))
    rval = random.uniform(-999999, 999999)
    response = nm.via_json.prepare_sensor_data(id_in=rid, value=rval)
    assert response == {"id": rid, "value": rval}


def test_json_prepare_sensor_data_filled(nm_initialized):
    nm = nm_initialized
    rid = random_string(random.randint(1, 20))
    rval = random.uniform(-999999, 999999)
    runit = random_string(random.randint(1, 3))
    rutc = random.randint(0, 999999999)
    response = nm.via_json.prepare_sensor_data(id_in=rid, value=rval, unit=runit, utc_time=rutc)
    assert response == {"id": rid, "value": rval, "unit": runit, "time": rutc}


def test_json_prepare_data_short_with_mac(nm_initialized, sensor_data):
    nm = nm_initialized
    sdata = sensor_data()
    rmac = random_string(random.randint(1, 20))
    response = nm.prepare_data_short(sensors=sdata, mac=rmac)
    assert response == {"devices": [{"mac": rmac, "sensors": sdata}]}


def test_json_prepare_data_short_without_mac(nm_initialized, sensor_data):
    nm = nm_initialized
    sdata = sensor_data()
    response = nm.via_json.prepare_data_short(sensors=sdata)
    assert response == {"devices": [{"mac": nm.via_json.mac, "sensors": sdata}]}


def test_json_prepare_device_data_full_filled(nm_initialized, sensor_data):
    nm = nm_initialized
    sdata = sensor_data()
    rmac = random_string(random.randint(1, 20))
    rowner = random_string(random.randint(1, 20))
    rname = random_string(random.randint(1, 20))
    rlon = random.uniform(-180, 180)
    rlat = random.uniform(90, 90)
    ralt = random.uniform(-4000, 9000)

    response = nm.via_json.prepare_device_data_full(sensors=sdata, mac=rmac, name=rname, owner=rowner, lat=rlat,
                                                    lon=rlon, alt=ralt)
    assert response == {"mac": rmac, "name": rname, "owner": rowner, "lat": rlat, "lon": rlon, "alt": ralt,
                        "sensors": sdata}


def test_json_prepare_device_data_full_default(nm_initialized, sensor_data):
    nm = nm_initialized
    sdata = sensor_data()
    response = nm.via_json.prepare_device_data_full(sensors=sdata)
    assert response == {"mac": nm.via_json.mac, "name": nm.via_json.name, "owner": nm.via_json.owner,
                        "lat": nm.via_json.lat, "lon": nm.via_json.lon, "alt": nm.via_json.alt,
                        "sensors": sdata}



latitude = 55.4005523
longitude = 37.8104
altitude = 165

name = "wwakabobik_ws"
owner = "Iliya Vereshchagin"
mac = "b8:27:eb:06:17:26"

nm = Narodmon(mac=mac, name=name, owner=owner, lat=latitude, lon=longitude, alt=altitude)
sdata = nm.via_json.prepare_sensor_data(id_in="TEMPC", value=-5.78)
print(sdata)
ddata = nm.via_json.prepare_device_data_full(sensors=sdata)
print(ddata)
response = nm.via_json.send_full_data_json(sensors=sdata)
print(response)
