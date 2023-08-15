""" Python client for Eagle Eye Networks APIv3 """
version = "0.0.11"
__version__ = version


import json
import logging
import requests

from datetime import datetime, timedelta
from pytz import timezone

from io import BytesIO

logging.basicConfig(level=logging.INFO)



class EagleEyev3():
    """
    Class representing the EagleEyev3 client.
    """

    __version__ = version
    __all__ = ['EagleEyev3', 'Device', 'Camera']

    def __init__(self, config=None):
        """
        Initializes the EagleEyev3 client object.
        """
        self.client_id = None
        self.client_secret = None
        self.access_token = None
        self.reseller_access_token = None # this is the reseller user they switched from
        self.refresh_token = None
        self.redirect_uri = None

        keys_to_check = ['client_id', 'client_secret', 'server_protocol', 'server_host', 'server_port', 'server_path']
        if config and all([name in config for name in keys_to_check]):
            self._load_vars_from_settings(config)
        else:
            if config is None:
                logging.warn("config is None or was not passed into constructor")
            else:
                logging.error("config is missing keys")

        self.user_base_url = None
        self.current_user = None
        self.users = []
        self.bridges = []
        self.cameras = []
        self.switches = []
        self.users = []
        self.active_account = None
        self.accounts = []
        self.user_tz_obj = None

        self.lazy_login = False

        if self.lazy_login:
            try:
                self._load_access_token()
            except FileNotFoundError as e:
                logging.warn("self.lazy_login is set to {self.lazy_login} but could not find .lazy_login file to load")

        # for use with request calls, can be an int, tuple, or None
        # preferred would be a tuple with the first value is time to connect, second is time to first byte
        # https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
        # called by self._get_timeout_values
        self.timeout_values = {
            'default': (3,5),
            'login': (5, 30),
            'logout': (5, 15),
            'list_of_events': (6, 20),
            'live_preview': (3, 5),
            'switch_account': (5, 30)
        }

    def _load_vars_from_settings(self, config={}):
        """
        Load variables from the settings module.
        """
        self.client_id = config['client_id']
        self.client_secret = config['client_secret']
        self.server_protocol = config['server_protocol']
        self.server_host = config['server_host']
        self.server_port = config['server_port']
        self.server_path = config['server_path']

        # Combine server_protocol, server_host, and server_port to make the redirect_uri
        # Note: Please see the note in settings.py about trailing slashes and modify this line if needed
        
        self.redirect_uri = f"{self.server_protocol}://{self.server_host}:{self.server_port}/{self.server_path}"

    def _save_access_token(self):
        with open(".lazy_login", "w") as json_file:
            json.dump({
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'current_user': self.current_user
            }, json_file)

    def _load_access_token(self):
        with open(".lazy_login", "r") as json_file:
            saved = json.load(json_file)
            if 'access_token' in saved:
                self.access_token = saved['access_token']
            if 'refresh_token' in saved:
                self.refresh_token = saved['refresh_token']

        self.get_base_url(cascade=True)

    def time_now(self):
        return datetime.now(tz=self.user_tz_obj).isoformat(timespec='milliseconds')

    def time_before(self, ts=None, hours=6):
        if ts == None:
            ts = datetime.now(tz=self.user_tz_obj)

        if type(ts) == str:
            ts = datetime.fromisoformat(ts)

        return (ts - timedelta(hours=hours)).isoformat(timespec='milliseconds')

    def login_tokens(self, code=None, cascade=True):
        """
        Obtains login tokens using the authorization code.

        Args:
            code (str): The authorization code.
            cascade (bool): Indicates whether to cascade and get the base URL and current user information.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, data, and current user information.
        """
        baseUrl = "https://auth.eagleeyenetworks.com/oauth2/token"
        pathUrl = f"?grant_type=authorization_code&scope=vms.all&code={code}&redirect_uri={self.redirect_uri}" # Note the trailing slash, make sure it matches the whitelist
        url = baseUrl + pathUrl

        # Send a POST request to obtain login tokens
        response = requests.post(url, auth=(self.client_id, self.client_secret), timeout=self._get_timeout_values('login'))
        response_json = response.json()

        logging.info(f"{response.status_code} in login_tokens")

        if response.status_code == 200:
            success = True
            self.access_token = response_json['access_token']
            self.refresh_token = response_json['refresh_token']

            if self.lazy_login:
                self._save_access_token()

            if cascade:
                self.get_base_url(cascade=cascade)
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json,
            'current_user': self.current_user
        }

    def logout(self):
        """
        Revokes token.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = "https://auth.eagleeyenetworks.com/oauth2/revoke"

        payload = {
            "token": self.access_token,
            "token_type_hint": "access_token"
        }

        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json",
                    "Content-type": "application/json"
                }

        # Send a POST request to obtain the base URL
        response = requests.post(url, json=payload, headers=headers, timeout=self._get_timeout_values('logout'))
        response_json = response.json()

        logging.info(f"{response.status_code} in logout")

        if response.status_code == 200:
            success = True
        else:
            success = False
            logging.info(f"call to logout: {response_json}")

        self.access_token = None
        self.refresh_token = None

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def login_from_reseller(self, target_account_id=None, cascade=True):
        """
        Obtains acces_token for a end-user account.

        Args:
            code (str): The authorization code.
            target_account_id (str): Account ID that you want to get access to.
            cascade (bool): Indicates whether to cascade and get the base URL and current user information.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, data, and current user information.
        """
        url = "https://auth.eagleeyenetworks.com/api/v3.0/authorizationTokens"

        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        payload = {
            "type": "reseller",
            "targetType": "account",
            "targetId": target_account_id,
            "scopes": [
                "vms.all"
            ]
        }

        # Send a POST request to obtain login tokens
        response = requests.post(url, headers=headers, json=payload, timeout=self._get_timeout_values('switch_account'))
        response_json = response.json()

        logging.info(f"{response.status_code} in login_from_reseller")

        if response.status_code == 201: # POST is expected to return a 201
            success = True
            self.reseller_access_token = self.access_token
            self.access_token = response_json['accessToken']
            self.active_account = target_account_id

            if self.lazy_login:
                self._save_access_token()

            if cascade:
                self.get_base_url(cascade=cascade)
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json,
            'current_user': self.current_user
        }

    def get_base_url(self, cascade=True):
        """
        Obtains the base URL for the user.

        Args:
            cascade (bool): Indicates whether to cascade and get the current user information.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = "https://api.eagleeyenetworks.com/api/v3.0/clientSettings"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        try:
            # Send a GET request to obtain the base URL
            response = requests.get(url, headers=headers, timeout=self._get_timeout_values('base_url'))
            response_json = response.json()

            logging.info(f"{response.status_code} in get_base_url")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for {self.id} get_base_url()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        if response.status_code == 200:
            success = True
            if 'httpsBaseUrl' in response_json and 'hostname' in response_json['httpsBaseUrl']:
                self.user_base_url = response_json['httpsBaseUrl']['hostname']
                if cascade:
                    self.get_current_user()
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_current_user(self):
        """
        Obtains the information of the current user.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/users/self?include=timeZone"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        try:
            # Send a GET request to obtain the current user information
            response = requests.get(url, headers=headers, timeout=self._get_timeout_values('curent_user'))
            response_json = response.json()

            logging.info(f"{response.status_code} in get_current_user")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for get_current_user()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        if response.status_code == 200:
            success = True
            self.current_user = response_json
            self.user_tz_obj = timezone(response_json['timeZone']['timeZone'])

            if self.active_account is None:
                self.active_account = response_json['accountId']


        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_users(self):
        """
        Obtains the list of users.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/users?include=timeZone"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        try:
            response = requests.get(url, headers=headers, timeout=self._get_timeout_values('list_of_users'))
            response_json = response.json()

            logging.info(f"{response.status_code} in get_list_of_users")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for get_list_of_users()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        if response.status_code == 200:
            success = True
            self.users = [i for i in response_json['results']]
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_accounts(self):
        """
        Obtains the list of accounts.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/accounts"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        try:
            response = requests.get(url, headers=headers, timeout=self._get_timeout_values('list_of_accounts'))
            response_json = response.json()

            logging.info(f"{response.status_code} in get_list_of_accounts")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for get_list_of_accounts()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        if response.status_code == 200:
            success = True
            self.accounts = [i for i in response_json['results'] if i not in self.accounts] + self.accounts
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_cameras(self):
        """
        Obtains the list of cameras.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """

        includes = ''.join(['status'])
        page_size = 1000
        nextPageToken = None

        # emulating a do while toop in order to handle pagination, remember to break out of this loop
        while True:

            if nextPageToken:
                url = f"https://{self.user_base_url}/api/v3.0/cameras?include={includes}&pageSize={page_size}&pageToken={nextPageToken}"
            else:
                url = f"https://{self.user_base_url}/api/v3.0/cameras?include={includes}&pageSize={page_size}"

            headers = { 
                        "Authorization": f"Bearer {self.access_token}", 
                        "Accept": "application/json"
                    }

            response = self._make_get_request(url=url, headers=headers, timeout='list_of_cameras')

            if response:
                response_json = response.json()

                logging.info(f"{response.status_code} in get_list_of_cameras")

            else:
                return {
                    "success": False,
                    "response_http_status": 0,
                    "data": None
                }


            if response.status_code == 200:
                success = True
                self.cameras = self.cameras + [
                        Camera(id=i['id'],\
                               name=i['name'],\
                               status=i['status'],\
                               account_id=i['accountId'],\
                               bridge_id=i['bridgeId'],\
                               user_base_url=self.user_base_url,\
                               een_instance=self)
                               for i in response_json['results'] if i['id'] not in [j.id for j in self.cameras]]

                for camera in self.cameras:
                    camera.user_base_url = self.user_base_url

                if 'nextPageToken' in response_json and len(response_json['nextPageToken']) > 0:
                    nextPageToken = response_json['nextPageToken']
                else:
                    break

            else:
                success = False
                break

        
        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def _make_get_request(self, url=None, headers={}, timeout='default'):
        try:
            response = requests.get(url, headers=headers, timeout=self._get_timeout_values(timeout))
            return response

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired get_list_of_cameras()")
            return None

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return None

    def get_list_of_bridges(self):
        """
        Obtains the list of bridges.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/bridges"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        try:
            response = requests.get(url, headers=headers, timeout=self._get_timeout_values('list_of_bridges'))
            response_json = response.json()

            logging.info(f"{response.status_code} in get_list_of_bridges")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for get_list_of_bridges()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        if response.status_code == 200:
            success = True
            self.bridges = [i for i in response_json['results']]
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_switches(self):
        """
        Obtains the list of switches.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/switches"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        try:
            response = requests.get(url, headers=headers, timeout=self._get_timeout_values('list_of_switches'))
            response_json = response.json()

            logging.info(f"{response.status_code} in get_list_of_switches")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for get_list_of_switches()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        if response.status_code == 200:
            success = True
            self.switches = [i for i in response_json['results']]
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_available_devices(self, deviceType__in="camera"):
        """
        Obtains the list of available devices.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/availableDevices?deviceType__in={deviceType__in}"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        try:
            response = requests.get(url, headers=headers, timeout=self._get_timeout_values('list_of_available_devices'))
            response_json = response.json()

            logging.info(f"{response.status_code} in get_list_of_available_devices")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for get_list_of_available_devices()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        if response.status_code == 200:
            success = True
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_multi_cameras(self):
        """
        Obtains the list of multi-cameras.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/multiCameras"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        try:
            response = requests.get(url, headers=headers, timeout=self._get_timeout_values('list_of_multi_cameras'))
            response_json = response.json()

            logging.info(f"{response.status_code} in get_list_of_multi_cameras")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for get_list_of_multi_cameras()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        if response.status_code == 200:
            success = True
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_list_of_feeds(self):
        """
        Obtains the list of feeds.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """
        url = f"https://{self.user_base_url}/api/v3.0/feeds"
        headers = { 
                    "Authorization": f"Bearer {self.access_token}", 
                    "Accept": "application/json"
                }

        try:
            response = requests.get(url, headers=headers, timeout=self._get_timeout_values('list_of_feeds'))
            response_json = response.json()

            logging.info(f"{response.status_code} in get_list_of_feeds")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for get_list_of_feeds()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        if response.status_code == 200:
            success = True
        else:
            success = False

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }

    def get_camera_by_id(self, esn):
        found_camera = None
        for camera in self.cameras:
            if camera.id == esn:
                found_camera = camera
                break

        if found_camera == None:
            camera = Camera()

        logging.debug(f"returning camera {camera} for search query {esn}")
        return camera

    def _get_timeout_values(self, name='default'):
        if name in self.timeout_values:
            return self.timeout_values[name]
        else:
            return self.timeout_values['default']



class Device():

    def __init__(self, id=None, name=None, status=dict(), account_id=None, user_base_url=None, een_instance=None):

        self.id = id
        self.name = name
        self.status = status
        self.account_id = account_id
        self.user_base_url = user_base_url,
        self.een_instance = een_instance

    def get_id(self):
        return self.id

    def get_status(self):
        if 'connectionStatus' in self.status:
            return self.status['connectionStatus']
        return None

    def is_online(self):
        if 'connectionStatus' in self.status:
            return self.status['connectionStatus'] == "online"
        return None

    def is_offline(self):
        if 'connectionStatus' in self.status:
            return self.status['connectionStatus'] == "deviceOffline" \
                or self.status['connectionStatus'] == "bridgeOffline" \
                or self.status['connectionStatus'] == "error"
        return None

    def __repr__(self):
        if self.is_online():
            online = '✅'
        elif self.is_offline():
            online = '❌'
        else:
            online = '？'
        return f"{online} [{self.id}] - {self.name}"



class Camera(Device):

    def __init__(self, id=None, name=None, status=dict(), account_id=None, bridge_id=None, user_base_url=None, een_instance=None):
        super().__init__(id=id, name=name, status=status, account_id=account_id, user_base_url=user_base_url, een_instance=een_instance)
        self.bridge_id = bridge_id
        self.previews = []
        self.videos = []
        self.events = {
                'status': [],
                'motion': []
                }
    
    
    def get_list_of_events(self, start_timestamp=None, end_timestamp=None):
        """
        Obtains the list of events.

        Returns:
            dict: Dictionary containing the success status, response HTTP status code, and data.
        """

        if start_timestamp == None or end_timestamp == None:
            logging.debug(f"get_list_of_events called without timestamp")
            return {
                "success": False,
                "response_http_status": None,
                "data": { 'msg': 'get_list_of_events called without required args, needs start_timestamp, end_timestamp' }
            }

        url = f"https://{self.user_base_url}/api/v3.0/events?pageSize=100&include=een.deviceCloudStatusUpdate.v1&startTimestamp__gte={start_timestamp}&endTimestamp__lte={end_timestamp}&actor=camera%3A{self.id}&type__in=een.deviceCloudStatusUpdateEvent.v1"

        headers = { 
                    "Authorization": f"Bearer {self.een_instance.access_token}", 
                    "Accept": "application/json"
                }

        try:
            response = requests.get(url, headers=headers, timeout=self.een_instance._get_timeout_values('list_of_events'))
            response_json = response.json()

            logging.debug(f"{response.status_code} returned from {url} with {headers} and {response.text}")
            logging.info(f"{response.status_code} in get_list_of_events")

            if response.status_code == 200:
                success = True
                # filter events by type
                [self.events['status'].append(i) for i in response.json()['results'] if i['type'] == 'een.deviceCloudStatusUpdateEvent.v1']
                [self.events['motion'].append(i) for i in response.json()['results'] if i['type'] == 'een.motionDetectionEvent.v1']

                # remove duplicates
                seen = set()
                self.events['status'] = [event for event in self.events['status'] if event['id'] not in seen and not seen.add(event['id'])]

                seen = set()
                self.events['motion'] = [event for event in self.events['motion'] if event['id'] not in seen and not seen.add(event['id'])]

                # sort by event startTimestamp descending
                self.events['status'] = sorted(self.events['status'], key=lambda x: x['startTimestamp'], reverse=True)
                self.events['motion'] = sorted(self.events['motion'], key=lambda x: x['startTimestamp'], reverse=True)
            else:
                success = False

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for {self.id} get_list_of_events()")
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }

        except requests.exceptions.RequestException as e:
            logging.warn(e)
            return {
                "success": False,
                "response_http_status": 0,
                "data": None
            }
            

        return {
            "success": success,
            "response_http_status": response.status_code,
            "data": response_json
        }


    def get_live_preview(self):

        url = f"https://{self.user_base_url}/api/v3.0/media/liveImage.jpeg?deviceId={self.id}&type=preview"

        headers = { 
                    "Authorization": f"Bearer {self.een_instance.access_token}", 
                    "Accept": "image/jpeg"
                }

        try:
            response = requests.get(url, headers=headers, timeout=self.een_instance._get_timeout_values('live_preview'))
            logging.info(f"{response.status_code} in get_live_preview")

        except requests.exceptions.Timeout:
            logging.warn(f"timeout expired for {self.id} get_live_preview()")
            response = None
        
        except requests.exceptions.RequestException as e:
            logging.warn(e)
            response = None
        
        return response








