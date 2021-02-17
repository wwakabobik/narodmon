**Simple python wrapper around narodmon's APIs**

## Requirements

You need to register in https://narodmon.ru/
If you plan to use /api endpoint, you need to get api key also.
Narodmon contains two endpoints - json and api. This wrapper provides wrap for both of them.


## Usage

Import `Narodmon` class, which contains all api methods:

    from narodmon import Narodmon

#### JSON endpoint

This endpoint is used for uploading sensors data.
To achieve more security, this wrapper uses https secure connection with POST JSON requests only. If you plan to use something else, feel free to enhance this package or fork.

To succeed with JSON endpoint, you need to specify:
- `mac` address of device (should be unique and hidden)
- `name` of device (any string)
- `owner` of the device (any string)
- `lat` - latitude where device is placed
- `lon` - longitude where device is placed
- `alt` - altitude where device is placed

If so, it's better to init class like
 

    nm = Narodmon(mac=mac, lat=lat, lon=lon, 
                  alt=alt, owner=owner, name=name)
    
Optional, you can leave any or all params blank. You can set them any time via `set` methods:
    
    nm.via_json.set_mac(mac)
    nm.via_json.set_name(name)
    nm.via_json.set_owner(owner)
    nm.via_json.set_lat(lat)
    nm.via_json.set_lon(lon)
    nm.via_json.set_alt(alt) 

Prior to send data, you must pack it in related dicts, first of all, sensors data can be packed via:

    sensor_data = nm.via_json.prepare_sensor_data(id_in=id, 
                                                  value=val, unit=unit, utc_time=utc)
    # 'unit' optional when id_in used with recommended names (refer to docs or 
    # settings.py dict). 'utc_time' is optional, if sensor measurement is now.
    # sensor data will be dict like: {'id': 'TEMPC', 'value': -5.78}

Secondly, you can pack multiple sensors data for each device. To achieve it, use lists:

    sensors = [sensor_data1, sensor_data2]
    
When you prepare all sensor data, you can send data for whole device:

    response = nm.via_json.send_full_data_json(sensors=sensors)   # full data send (only for first call)
    response = nm.via_json.send_short_data_json(sensors=sensors)  # short sensors data send (without device data)
    
Alternatively, you can prepare data for several devices and send it bulk:

    
    device1 = nm.via_json.prepare_device_data_full(sensors=sensors1, mac=mac1, name=name1, 
                                                   owner=owner1, lat=rlat, lon=lon1, alt=alt1)
    device2 = nm.via_json.prepare_device_data_short(sensors=sensors2, mac=mac2)
    devices = [device1, device2]
    response = nm.via_json.send_bulk_data(data=devices)
        
#### REST API endpoint

This endpoint is used for manage narodmon, devices (sensors, cameras), obtain and send data.
To achieve more security, this wrapper uses https secure connection with POST JSON requests only. If you plan to use something else, feel free to enhance this package or fork.

To succeed with REST API endpoint, you need to specify:
- `uuid` - unique id of device
- `api_key` obtained from service
- `lang` - (optional) default language, may be 'ru', 'en', 'uk'
- `lat` - (optional) latitude where device is placed
- `lon` - (optional) longitude where device is placed

self.via_api = InterfaceAPI(uuid=uuid, api_key=api_key, lang=lang, lat=lat, lon=lon)

If so, it's better to init class like
 
    nm = Narodmon(uuid=uuid, api_key=api_key, lang=lang, lat=lat, lon=lon)

Optional, you can leave any or all params blank. You can set them any time via `set` methods:
    
    nm.via_api.set_uuid(uuid)
    nm.via_api.set_api_key(api_key)
    nm.via_api.set_lang(lang)
    nm.via_api.set_lat(lat)
    nm.via_api.set_lon(lon)

Actually, service assume that `uuid` is MD5 hash, not pure name. To convert string-like uuid to hash, use following method:
    
    uuid_hash = nm.via_api.encrypt_uuid()
    # method will replace stored uuid with hash, so you do not need to update it manually


To send weather measurements use following:

    nm.via_api.weather_report(lat=lat, lon=lon, temp=temp_in_c, humid=humid, press=pressure, wind=wind_heading,
                              lang=lang, api_key=api_key, uuid=uuid)
    # If you fully init Narodmon class, lat, lon, api_key, uuid, lang params are optional
    # Sensors params also optional, you can specify one of them or all to send all
    
All other methods also wrapped, please use inline docs or refer to service.


#### Troubleshooting

Please read service API docs first. Most probably, all of the problems are related to wrong data and API send limit (1-5 min).
Each server response checked by inline function, so, if error occured, it will be redirected to stderr. 

    
## Terms of service

Refer to 
https://narodmon.ru/
