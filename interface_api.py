import requests

from narodmon.tools import status_decode, generate_hash
from narodmon.settings import BASE_API_URL


class InterfaceAPI:
    def __init__(self, uuid, api_key, lang, lat=None, lon=None):
        self.endpoint = f'{BASE_API_URL}/api'
        self.uuid = uuid,
        self.api_key = api_key
        self.lang = lang
        self.lat = lat
        self.lon = lon

    def set_uuid(self, uuid):
        """
        Set/update default uuid
        :param uuid: unique id (MD5 hash)
        """
        self.uuid = uuid

    def set_api_key(self, api_key):
        """
        Set/update default api_key
        :param api_key: API key provided by narodmon
        :return:
        """
        self.api_key = api_key

    def set_lang(self, lang):
        """
        Set/update default language:
        :param lang: string, possible values are: "ru","en","uk"
        """
        self.lang = lang

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

    def prepare_default_payload(self, uuid=None, api_key=None, lang=None, ignore_lang=False):
        """
        Generate dict with default payload (uuid, api key should be transmitted in every and each request).
        If none params specified - default params will be used.
        :param uuid: (optional) unique identifier
        :param api_key: (optional) api key provided by narodmon
        :param lang: (optional) language, string, possible values are: "ru","en","uk"
        :param ignore_lang: (optional) bool, if True - language will not be added to payload
        :return:
        """
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
        """
        Send post request and check it response
        :param payload: payload in json format
        :return: response JSON
        """
        response = requests.post(url=self.endpoint, json=payload)
        status_decode(response)
        return response.json()

    def app_init(self, lang=None, version=None, platform=None, model=None, width=None, utc=None, api_key=None,
                 uuid=None):
        """
        Проверка актуальности версии приложения при первом запуске и раз в сутки, проверка авторизации пользователя,
        его местонахождения, избранного и справочник типов датчиков.
        Параметры запроса:
            - version версия приложения пользователя для контроля, например: 1.1;
            - platform версия платформы(ОС), например 6.0.1;
            - model модель устройства, например Xiaomi Redmi Note 4;
            - width ширина экрана клиентского устройства в пикселях для оптимизации размера загружаемых изображений;
            - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk");
            - utc часовой пояс пользователя приложения в UTC (смещение в часах).

            ОТВЕТ сервера:
            - latest актуальная версия приложения указанная в Мои приложения;
            - url скачивания обновления приложения указанный в Мои приложения;
            - login имя авторизованного пользователя для данного uuid иначе "";
            - vip = 1 признак партнера, донатора, разработчика, администрации, для остальных = 0;
            - lat, lon широта и долгота текущего местонахождения пользователя в десятичном виде;
            - addr ближайший адрес текущего местонахождения пользователя;
            - timestamp текущее время сервера в UnixTime (для сверки);
            - types[..] справочник типов датчиков;
            - types[type] код типа датчика;
            - types[name] название типа датчика;
            - types[unit] единица измерения;
            - favorites[..] массив из ID избранных датчиков у авторизованного пользователя.

        App comparison request
        :param lang: (optional) language, string, may be "ru", "uk", "en"
        :param version: (optional) version of app
        :param platform: (optional) platform version
        :param model: (optional) model of device
        :param width: (optional) width of device screen
        :param utc: (optional) utc shift
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
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
        """
        Запрос списка датчиков и веб-камер в указанной прямоугольной области карты
        Параметры запроса:
            - bounds массив координат углов области просмотра {широта-мин, долгота-мин, широта-макс, долгота-макс}
              в десятичном виде;
            - limit кол-во датчиков, веб-камер в ответе сервера, по умолчанию 20, максимум 50
              (используется серверная кластеризация);
            - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk").

            ОТВЕТ сервера:
            - devices массив с перечнем приборов и их датчиков в выбранной области просмотра;
            - devices[id] целочисленный код прибора в проекте;
            - devices[name] название прибора или его ID (если нет названия);
            - devices[lat], devices[lon] широта и долгота прибора в десятичном виде;
            - devices[time] время последнего показания датчика в UnixTime;
            - devices[value] показание датчика для балуна прибора (с макс приоритетом);
            - devices[type] код типа датчика (см. appInit);
            - devices[unit] единица измерения;
            - webcams массив с перечнем веб-камер в выбранной области просмотра;
            - webcams[id] целочисленный код веб-камеры в проекте;
            - webcams[name] название веб-камеры (как назвал владелец);
            - webcams[lat], webcams[lon] широта и долгота веб-камеры в десятичном виде;
            - webcams[time] время последней загрузки снапшота на сервер в UnixTime;
            - webcams[image] URL последнего снимка с веб-камеры.

        Get devices (sensors and webcams in selected rect)
        :param bounds: array of coordinates should be [lat-min, lon-min, lat-max, lon-max]
        :param limit: maximum items in response, default = 20, max = 50
        :param lang: (optional) default language, string, may be "ru", "uk", "en"
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "mapBounds"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        payload.update({"bounds": bounds, "limit": limit, "lang": lang})
        return self.send_post_request(payload)

    def sensors_nearby(self, lang=None, lat=None, lon=None, my=None, pub=None, radius=None, limit=None, types=None,
                       trends=None, uuid=None, api_key=None):
        """
        Запрос списка ближайших к пользователю датчиков + свои + избранные
        * Для доступа к данным ваших приватных датчиков вне вашей локальной сети требуется однократная авторизация
          (userLogon).

        Параметры запроса:
        - lat, lon опционально широта и долгота нового местонахождения пользователя в десятичном виде;
        - my опционально, если = 1, то вывод датчиков только со своих приборов (требуется авторизация);
        - pub опционально, если = 1, то вывод только публичных датчиков;
        - radius опционально максимальное удаление от пользователя до датчиков в км, максимум ~111км (1°);
        - limit опционально максимальное кол-во ближайших публичных приборов мониторинга в ответе сервера,
          по умолчанию 20, максимум 50;
        - types опционально массив кодов типов датчиков для фильтра отображения из справочника appInit;
        - trends = 1, необязательный параметр включающий расчет тендеции показаний;
        - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk").

        ОТВЕТ сервера:
        - devices массив с перечнем приборов, к которым подключены публичные или свои датчики;
        - devices[id] целочисленный код прибора в проекте;
        - devices[name] название прибора или его ID (если нет названия);
        - devices[my] = 1, если этот прибор авторизованного пользователя, иначе = 0;
        - devices[owner] ID владельца прибора в проекте;
        - devices[mac] серийный номер прибора (только для владельца);
        - devices[cmd] = 1, если включен режим управления прибором, иначе = 0;
        - devices[location] населенный пункт местонахождения прибора;
        - devices[distance] расстояние в км от текущего местонахождения пользователя;
        - devices[time] время последней активности прибора в UnixTime;
        - devices[lat], devices[lon] широта и долгота расположения прибора в десятичном виде;
        - devices[sensors] массив с перечнем публичных и своих датчиков, подключенных к данному прибору;
        - devices[sensors][id] целочисленный код датчика в проекте;
        - devices[sensors][mac] метрика датчика (только для владельца);
        - devices[sensors][fav] = 1, если датчик в Избранном у пользователя и = 0, если нет или не авторизован;
        - devices[sensors][pub] = 1, если датчик публичный и = 0, если датчик приватный;
        - devices[sensors][type] код типа датчика (см. appInit);
        - devices[sensors][name] название датчика или его ID (если нет названия);
        - devices[sensors][value] последнее показание датчика;
        - devices[sensors][unit] единица измерения;
        - devices[sensors][time] время последнего показания датчика в UnixTime;
        - devices[sensors][changed] время последнего изменения показаний датчика в UnixTime;
        - devices[sensors][trend] коэффициент линейного роста показаний датчика за последний час, рассчитанный по МНК.

        Get sensors nearby
        :param lat: (optional) latitude of user (float)
        :param lon: (optional) longitude of user (float)
        :param my: if == 1, then only own sensors will be selected
        :param pub: if == 1, then only public sensors will be selected
        :param radius: radius away from user (0-111km)
        :param limit: maximum items in response, default = 20, max = 50
        :param types: list of sensor id's [id1, id2], may be obtained via app_init
        :param trends: if == 1 then trending data will be selected
        :param lang: (optional) default language, string, may be "ru", "uk", "en"
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
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
        """
        Запрос списка датчиков и их показаний по ID прибора
        * Для доступа к данным ваших приватных датчиков вне вашей локальной сети требуется однократная авторизация
          (userLogon).
        Параметры запроса:
        - id ID прибора из ссылки вида https://narodmon.ru/id в балуне на карте;
        - trends = 1, необязательный параметр включающий расчет тендеции показаний;
        - info = 1, необязательный параметр включает вывод полного описания прибора;
        - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk").

        ОТВЕТ сервера:
        - id ID прибора в проекте;
        - name название прибора или его ID (если нет названия);
        - my = 1, если этот прибор авторизованного пользователя, иначе = 0;
        - owner ID владельца прибора в проекте;
        - mac серийный номер прибора (только для владельца);
        - cmd = 1, если включен режим управления прибором, иначе = 0;
        - location населенный пункт местонахождения прибора;
        - distance расстояние в км от текущего местонахождения пользователя;
        - time время последней активности прибора в UnixTime;
        - site ссылка на сайт владельца прибора, иначе https://narodmon.ru/id;
        - photo ссылка на фото прибора (если владелец его загрузил), иначе пустая строка;
        - info описание прибора (если info = 1), иначе длина описания в байтах или пустая строка;
        - sensors массив датчиков подключенных к указанному прибору;
        - sensors[id] целочисленный код датчика в проекте;
        - sensors[pub] = 1, если датчик публичный и = 0, если датчик приватный;
        - sensors[type] код типа датчика (см. appInit);
        - sensors[name] название датчика или его ID (если нет названия);
        - sensors[value] последнее показание датчика;
        - sensors[unit] единица измерения;
        - sensors[time] время последнего показания датчика в UnixTime;
        - sensors[changed] время последнего изменения показаний датчика в UnixTime;
        - sensors[trend] коэффициент линейного роста показаний датчика за последний час, рассчитанный по МНК.


        :param id_in: id of device with connected sensors
        :param trends: if == 1 then trending data will be selected
        :param info: if == 1 then full sensor info will be displayed
        :param lang: (optional) default language, string, may be "ru", "uk", "en"
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "sensorsOnDevice", "id": id_in}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        if trends:
            payload.update({"trends": trends})
        if info:
            payload.update({"trends": info})
        return self.send_post_request(payload)

    def sensors_values(self, sensors, trends=None, api_key=None, uuid=None):
        """
        Регулярное обновление показаний выбранных датчиков
        * Для доступа к данным ваших приватных датчиков вне вашей локальной сети требуется однократная авторизация
          (userLogon).
        Параметры запроса:
        - sensors массив кодов датчиков для запроса показаний, max 50 датчиков;
        - trends = 1, необязательный параметр включающий расчет тендеции показаний.

        ОТВЕТ сервера:
        - sensors массив показаний запрошенных датчиков;
        - sensors[id] целочисленный код датчика в проекте;
        - sensors[type] код типа датчика (см. appInit);
        - sensors[value] последнее показание датчика;
        - sensors[time] время последнего показания датчика в UnixTime;
        - sensors[changed] время последнего изменения показаний датчика в UnixTime;
        - sensors[trend] коэффициент линейного роста показаний датчика за последний час, рассчитанный по МНК.

        Get sensor values
        :param sensors: array with sensor id's [id1, id2 ..]
        :param trends: if == 1 then trending data will be selected
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "sensorsValues", "sensors": sensors}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        if trends:
            payload.update({"trends": trends})
        return self.send_post_request(payload)

    def sensors_history(self, id_in, period, offset, api_key=None, uuid=None):
        """
        История показаний датчика за период (для графиков и тенденций)
        * Для доступа к данным ваших приватных датчиков вне вашей локальной сети требуется однократная авторизация
          (userLogon).
        Параметры запроса:
        - id код датчика для запроса истории показаний;
        - period название периода показаний: 'hour','day','week','month','year';
        - offset смещение по выбранному периоду в прошлое, т.е. 1(day) = вчера, 1(month) = прошл.месяц.

        ОТВЕТ сервера:
        - sensors массив запрошенных датчиков;
        - sensors[id] целочисленный код датчика в проекте;
        - sensors[type] код типа датчика (см. appInit);
        - sensors[name] название датчика или его ID (если нет названия);
        - sensors[unit] единица измерения;
        - data массив показаний запрошенного датчика;
        - data[id] целочисленный код датчика в проекте;
        - data[time] время показания датчика в UnixTime;
        - data[value] показание датчика в указанный момент времени.

        :param id_in: id of sensor
        :param period: type of period, may be 'hour','day','week','month','year'
        :param offset: offset back in history (depend on period type) (int)
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "sensorsHistory", "id": id_in, "period": period, "offset": offset}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def name_sensor(self, id_in, name=None, api_key=None, uuid=None):
        """
        Смена имени датчика (для владельца) или создание алиаса для остальных
        Параметры запроса:
        - id целочисленный код датчика в проекте;
        - name новое название датчика, если пустое, то меняется на по умолчанию.

        Rename sensor
        :param id_in: id of sensor
        :param name: new name of sensor, if none, default will be used
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "nameSensor", "id": id_in}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        if name:
            payload.update({"name": name})
        return self.send_post_request(payload)

    def webcams_nearby(self, lat=None, lon=None, limit=None, radius=None, width=None,
                       lang=None, api_key=None, uuid=None):
        """
        Запрос списка ближайших к пользователю веб-камер + свои + избранные
        Параметры запроса:
        - lat, lon опционально широта и долгота местонахождения пользователя в десятичном виде;
        - limit опционально максимальное кол-во ближайших публичных веб-камер в ответе сервера, по умолчанию 20,
          максимум 50;
        - radius опционально максимальное удаление от пользователя до веб-камеры в км, максимум ~111км (1°);
        - width опционально ширина экрана клиентского устройства в пикселях для оптимизации размера загружаемых снимков;
        - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk").

        ОТВЕТ сервера:
        - webcams массив с перечнем веб-камер;
        - webcams[id] целочисленный код веб-камеры в проекте;
        - webcams[name] название веб-камеры (как назвал владелец);
        - webcams[my] = 1, если веб-камера авторизованного пользователя, иначе = 0;
        - webcams[owner] ID владельца веб-камеры в проекте;
        - webcams[fav] = 1, если веб-камера в Избранном у пользователя и = 0, если нет или не авторизован;
        - webcams[distance] расстояние в км от текущего местонахождения пользователя;
        - webcams[location] населенный пункт местонахождения веб-камеры;
        - webcams[time] время последней загрузки снапшота на сервер в UnixTime;
        - webcams[lat], webcams[lon] широта и долгота расположения веб-камеры в градусах в десятичном виде;
        - webcams[image] URL последнего снимка с веб-камеры;

        Returns list of webcams nearby
        :param lat: (optional) latitude (float)
        :param lon: (optiona) longitude (float)
        :param limit: maximum of items in response, default = 20, max = 50
        :param radius: radius away from user (0-111km)
        :param width: width of user display, used for optimization of images
        :param lang: (optional) default language, string, may be "ru", "uk", "en"
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
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
        """
        Запрос списка снимков с веб-камеры по ее ID
        Параметры запроса:
        - id ID веб-камеры из ссылки вида http://narodmon.ru/-ID в балуне на карте;
        - limit опционально кол-во снимков в ответе сервера, по умолчанию 20, максимум 50;
        - since опционально время первого снимка в выборке в UnixTime, по умолчанию равно 0;
        - latest опционально время последнего снимка в выборке в UnixTime, по умолчанию равно текущему;
        - width опционально ширина экрана клиентского устройства в пикселях для оптимизации размера загружаемых снимков.

        ОТВЕТ сервера:
        - id целочисленный код веб-камеры в проекте;
        - name название веб-камеры (как назвал владелец);
        - location населенный пункт местонахождения веб-камеры;
        - distance расстояние в км от текущего местонахождения пользователя;
        - images массив снимков с веб-камеры находящихся на сервере;
        - images[time] время актуальности снимка в UnixTime;
        - images[image] URL для скачивания снимка.

        Returns webcam images url list
        :param id_in: id of webcam
        :param limit: maximum of items in response, default = 20, max = 50
        :param since: timestamp of first image in request (unixtime)
        :param latest: timestamp of last image in request (unixtime), by default = now
        :param width: width of user display, used for optimization of images
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
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
        """
        Авторизация пользователя в проекте и его регистрация
        Параметры запроса:
        - login логин пользователя для авторизации, если он не указан, то возвращается текущий логин для указанного
          uuid;
        - hash хэш для авторизации, вычисляется по формуле с объединением строк MD5(uuid + MD5(введенный пароль)),
          если хэш не указан, то считается запросом на регистрацию в проекте по email/sms;
        - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk").

        ОТВЕТ сервера:
        - vip = 1 признак партнера, донатора, разработчика, администрации, для остальных = 0;
        - login имя авторизованного пользователя для текущего uuid или пустая строка;
        - uid = ID участника проекта.

        Authorize user
        :param login: login of user
        :param hash: password hash (create it from string password via generate_hash_password(password))
        :param lang: (optional) default language, string, may be "ru", "uk", "en"
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "userLogon", "login": login, "hash": hash}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        return self.send_post_request(payload)

    def username(self, api_key=None, uuid=None, lang=None):
        """
        Запрос имени пользователя в проекте
        Параметры запроса:
        - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk").

        ОТВЕТ сервера:
        - vip = 1 признак партнера, донатора, разработчика, администрации, для остальных = 0;
        - login имя авторизованного пользователя для текущего uuid или пустая строка;
        - uid = ID участника проекта.

        Get username
        :param lang: (optional) default language, string, may be "ru", "uk", "en"
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: login (string)
        """
        payload = {"cmd": "userLogon"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        return self.send_post_request(payload)['login']

    def register_user(self, login, api_key=None, uuid=None, lang=None):
        """
        Регистрация пользователя в проекте
        Параметры запроса:
        - login логин пользователя для авторизации, если он не указан, то возвращается текущий логин для указанного
          uuid;
        - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk").

        ОТВЕТ сервера:
        - vip = 1 признак партнера, донатора, разработчика, администрации, для остальных = 0;
        - login имя авторизованного пользователя для текущего uuid или пустая строка;
        - uid = ID участника проекта.

        Register user
        :param login: login of user
        :param lang: (optional) default language, string, may be "ru", "uk", "en"
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "userLogon", "login": login}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        return self.send_post_request(payload)

    def user_location(self, lat=None, lon=None, addr=None, wifi=None, cells=None, gui=None,
                      lang=None, api_key=None, uuid=None):
        """
        Запрос текущего и установка нового местонахождение пользователя (точки отсчета)
        Параметры запроса:
        - lat, lon опционально широта и долгота местонахождения пользователя;
        - addr опционально ближайший адрес к местонахождению пользователя;
        - wifi опциональный массив точек доступа WiFi поблизости;
        - wifi[bssid] MAC адрес точки доступа;
        - wifi[rssi] уровень сигнала точки доступа в dBm (<0);
        - cells опциональный массив сотовых станций поблизости;
        - cells[bssid] = MCC[3]:MNC[3]:LAC[4]:CID[7] в hex виде;
        - cells[rssi] уровень сигнала сотовой станции в dBm (<0);
        - gui флаг указывающий на необходимость получения полного адреса;
        - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk").

        ОТВЕТ сервера:
        - lat, lon широта и долгота нового местонахождения пользователя в десятичном виде;
        - addr ближайший адрес к найденным координатам (при gui = 1).

        Request and set current location of user (via coordinates, wifi, or cell)
        :param lat: (optional) latitude (float)
        :param lon: (optional) longitude (float)
        :param addr: (optional) closest address to user
        :param wifi: array of wi-fi hotspots nearby user
        :param cells: array of cells station nearby user
        :param gui: if == 1 full address nearby user will be displayed
        :param lang: (optional) default language, string, may be "ru", "uk", "en"
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
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
        """
        Управление списком избранных датчиков и веб-камер
        Параметры запроса:
        - sensors опционально новый массив id избранных датчиков (список будет заменен, для его очистки передать
          "sensors":[0]);
        - webcams опционально новый массив id избранных веб-камер (список будет заменен, для его очистки передать
          "webcams":[0]);
        - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk").

        ОТВЕТ сервера:
        - sensors массив избранных датчиков авторизованного пользователя;
        - sensors[id] целочисленный код датчика в проекте, если <0 то удалить из списка;
        - sensors[type] код типа датчика (см. appInit);
        - sensors[name] название датчика или его ID (если нет названия);
        - sensors[value] последнее показание датчика;
        - sensors[unit] единица измерения;
        - sensors[time] время последнего показания датчика в UnixTime;
        - webcams массив избранных веб-камер авторизованного пользователя;
        - webcams[id] целочисленный код веб-камеры в проекте, если <0 то удалить из списка;
        - webcams[name] название веб-камеры или http-ссылка (как назвал владелец);
        - webcams[time] время последней загрузки снапшота на сервер в UnixTime;
        - webcams[image] URL последнего снимка с веб-камеры.

        Update or erase array of liked sensors and webcams
        :param sensors: (optional) new array of sensors, previous array will be updated, to erase - send [0]
        :param webcams: (optional)  new array of webcams, previous array will be updated, to erase - send [0]
        :param lang: (optional) default language, string, may be "ru", "uk", "en"
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "userFavorites"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        if type(sensors) == list:
            payload.update({"sensors": sensors})
        if type(webcams):
            payload.update({"webcams": webcams})
        return self.send_post_request(payload)

    def user_logout(self, api_key=None, uuid=None):
        """
        Завершение сеанса текущего пользователя
        Параметры запроса:
        * нет параметров *

        ОТВЕТ сервера:
        - login имя авторизованного пользователя для текущего uuid;
        - uid ID участника проекта.

        Logoff user
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "userLogout"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def add_like(self, id_in, api_key=None, uuid=None):
        """
        Отметка "Мне нравится" на снимках с веб-камер и приборах.
        Параметры запроса:
        - id веб-камеры(<0) или прибора(>0).

        ОТВЕТ сервера:
        - id веб-камеры(<0) или прибора(>0);
        - time время отметки в UnixTime;
        - liked общее число отметок "Нравится" на объекте после выполнения.

        Add like to device or webcam
        :param id_in: id of webcam or device
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "addLike", "id": id_in}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def dis_like(self, id_in, api_key=None, uuid=None):
        """
        Снятие отметки "Мне нравится" на снимках с веб-камер и приборах
        Параметры запроса:
        - id веб-камеры(<0) или прибора(>0).

        ОТВЕТ сервера:
        - id веб-камеры(<0) или прибора(>0);
        - time время снятия отметки в UnixTime;
        - liked общее число отметок "Нравится" на объекте после выполнения.

        Remove like from device of webcam
        :param id_in: id of webcam or device
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "disLike", "id": id_in}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def set_push_token(self, token, api_key=None, uuid=None):
        """
        Установка параметров отправки PUSH уведомлений. Используется FireBase (Android, iOS)
        Параметры запроса:
        - token токен для Android и iOS;

        Set push token
        :param token: token (firebase token)
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "setPushToken", "token": token}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def set_push_uri(self, uri, api_key=None, uuid=None):
        """
        Установка параметров отправки PUSH уведомлений. Используется WNS (Windows)
        Параметры запроса:
        - uri URL для Windows Mobile и Windows Phone.

        Set push uri
        :param uri: token (firebase token)
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "setPushURI", "uri": uri}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def set_push_status(self, states, api_key=None, uuid=None):
        """
        Параметры запроса:
        - states массив со статусами полученных сообщений:
        - states[id] идентификатор полученного сообщения (int unsigned);
        - states[time] время отправки сообщения в UnixTime;
        - states[status] код текущего статуса сообщения (201 - получено, 202 - прочтено).

        Set push status
        :param states: array with received messages statuses
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "setPushStatus", "states": states}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def send_command(self, id_in, command, api_key=None, uuid=None):
        """
        Отправка команды управления на прибор
        Параметры запроса:
        - id ID приборов в проекте (integer unsigned);
        - command строка команды, шаблон PCRE [a-z0-9_\-\+\=\;\/\.]+

        Send command to device
        :param id_in: id of device
        :param command: command usinf PCRE format
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "sendCommand", "id": id_in, "command": command}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def send_complaint(self, id_in, problem_time, name, email, problem, value, api_key=None, uuid=None):
        """
        Отправка жалобы на ошибочное показание датчика или снимка с веб-камеры
        Параметры запроса:
        - id код датчика (id>0) или веб-камеры (id<0);
        - time UnixTime времени возникновения проблемы;
        - name имя заявителя для обратной связи;
        - email почта заявителя для обратной связи;
        - problem краткое описание сути проблемы;
        - value каким должно быть показание датчика (для id>0).

        Send complaint due to device/webcam content
        :param id_in: id of device (device or webcam)
        :param problem_time: unixtime of problem
        :param name: name of reporter
        :param email: email of reporter
        :param problem: brief problem description
        :param value: what value should be
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "sendComplaint", "id": id_in, "time": problem_time, "name": name, "email": email,
                   "problem": problem, "value": value}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, ignore_lang=True))
        return self.send_post_request(payload)

    def send_message(self, subj, mess, uid=None, name=None, chat=None, email=None, images=None,
                     api_key=None, uuid=None):
        """
        Отправка сообщения в беседу или вопроса к Администрации
        Параметры запроса:
        - uid опционально ID получателя, по умолчанию Администрация;
        - name опционально имя заявителя для обращения;
        - email опционально почта заявителя для дублирования;
        - chat опционально ID беседы из getDialog;
        - subj обязательно тема обращения;
        - mess обязательно текст сообщения;
        - images[..] опционально массив вложенных изображений (до 1МБ) в виде base64 строк.

        Send message to user
        :param subj: message subject
        :param mess: message content
        :param uid: (optional) uid of reciever, by default = admin
        :param name: (optional) name of sender
        :param chat: (optional) id of chat in getDialog
        :param email: (optional) email of sender
        :param images: (optional) array of base64 images
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
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
        """
        Отправка метеоданных пользователем с автономных метеоприборов
        Параметры запроса:
        - lat, lon широта и долгота прибора на момент отправки (предварительно обновить геолокацию!);
        - temp показания уличного термометра (если он есть) °C;
        - humid показания уличного гигрометра (если он есть) %;
        - press показания бытового барометра (если он есть) мм рт.ст.;
        - wind азимут направления ветра (если есть анемометр) 0-360°;
        - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk").

        Send weather data
        :param lat: (optional) latitude (float)
        :param lon: (optiona) longitude (float)
        :param temp: (optional) temperature in celsius
        :param humid: (optional) relative humidity
        :param press: (optional) barometric pressure (mmgh)
        :param wind: (optional) wind heading
        :param lang: (optional) default language, string, may be "ru", "uk", "en"
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
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
        """
        Отправка отзыва на приложение и багрепортов с техданными для отладки
        Параметры запроса:
        - time опционально UnixTime момента возникновения сбоя;
        - name опционально имя заявителя для обращения;
        - email опционально почта заявителя для дублирования;
        - mess опционально текст сообщения пользователя;
        - logs опционально технические данные для отладки;
        - images[..] опционально массив вложенных изображений (до 1МБ) в виде base64 строк.

        Report bug
        :param time: (optional) unixtime when bug occured
        :param name: (optional) name of reporter
        :param email: (optional) email of reporter
        :param mess: (optiona) message
        :param logs: (optional) logs
        :param images: (optional) base64 images array
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
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

    def get_help(self, topic=None, lang=None, api_key=None, uuid=None):
        """
        Запрос справочной информации о проекте
        Параметры запроса:
        - topic опционально идентификатор статьи, если он не указан, то возвращается оглавление;
        - lang язык интерфейса приложения ISO 639-1 ("ru","en","uk").

        ОТВЕТ сервера:
        - topics массив со список статей;
        - topics[topic] идентификатор статьи;
        - topics[group] название раздела Справки;
        - topics[title] название статьи из Справки;
        - topics[body] html-текст статьи (если был указан topic) или хеш статьи в оглавлении.

        Get help article
        :param topic: if of article, if none is specified, table of contents will be displayed
        :param lang: (optional) default language, string, may be "ru", "uk", "en"
        :param api_key: (optional) api key provided by narodmon
        :param uuid: (optional) unique identifier MD5 hash
        :return: response JSON
        """
        payload = {"cmd": "getHelp"}
        payload.update(self.prepare_default_payload(uuid=uuid, api_key=api_key, lang=lang))
        if topic:
            payload.update({"topic": topic})
        return self.send_post_request(payload)

    def generate_hash_password(self, password, uuid=None):
        """
        Generate hash password from unencrypted password string and uuid

        :param password: uneqncrypted password string
        :param uuid: (optional) uuid, should be in MD5 hash formatted
        :return: MD5 hash
        """
        if not uuid:
            uuid = self.uuid
        return f'{uuid}{generate_hash(password)}'

    def encrypt_uuid(self):
        """
        Encrypt current uuid
        :return: none
        """
        self.uuid = generate_hash(self.uuid)
        return self.uuid
