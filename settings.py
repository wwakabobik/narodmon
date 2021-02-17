BASE_API_URL = 'https://narodmon.ru'

sensor_dict = {
    'temperature': ('TEMPC', 'BATTEMP', 'T*', 'TEMP*', 'BMPT*', 'DHTT*', 'DSW*', 'DS18T*'),
    'humidity': ('HUM', 'HUMID', 'RH', 'H*', 'RH*', 'DHTH*'),
    'pressure': ('HPA', 'PRESS', 'MMHG', 'BMPP'),
    'rain': ('RAIN', 'RAIN*'),
    'wind_speed': ('WS', 'KMH', 'WIND', 'WS*'),
    'heading': ('DEG', 'DIR'),
    'voltage': ('VOLT', 'VCC', 'UACC', 'VBAT', 'BATVOLT', 'U*', 'V*'),
    'current': ('I*', ),
    'power': ('P', 'W', 'P*', 'W*'),
    'power_energy': ('WH', 'KWH', 'WH*', 'KWH*'),
    'water_flow': ('WM', 'CWM', 'HWM', 'WM*'),
    'luminocity': ('LUX', 'LIGHT', 'L*'),
    'radiation': ('RAD', 'R*'),
    'logic': ('RELAY', 'S*', 'RL*', 'GPIO*', 'OUTPUT*', 'SIM*'),
    'net_traffic': ('RX', 'TX', 'RX*', 'TX*'),
    'air_concentration': ('CO', 'CO2', 'CH4', 'PPM', 'CO*'),
    'uptime': ('UPTIME', 'NOW', 'TIME', 'CURTIME', 'WORKTIME'),
    'signal_strength': ('DBM', 'RSSI', 'WIFI', 'GSM', 'SIGNAL'),
    'uv': ('UV', 'UV*'),
    'battery_status': ('BATCHARGE', 'MB2BAT'),
    'dust': ('DUST', 'PM', 'PM*'),
    'dew_point': ('DEW', 'DP', 'DP*'),
    'latitude': ('LAT',),
    'longitude': ('LON',),
    'altitude': ('ALT',)
}
