import json
import math
import requests

API_URL = "https://api-dev.3doptix.com/v1/"

class ThreedOptixAPI(object):
    def __init__(self, api_key):
        self.api_key = api_key

    def is_up(self):
        return healthcheck()[0]

    def get_setup_infos(self):
        data, message = get_setups(self.api_key)
        if data is not None:
            infos = []
            for info_json in data['setups']:
                infos.append((info_json['id'], info_json['name']))
            return infos
        else:
            raise Exception(message)

    def fetch_setup(self, setup_id):
        data, message = get_setup(setup_id, self.api_key)
        if data is not None:
            with open('example.opt', 'r') as f:
                setup_json = json.load(f)
                print(setup_json)
            return Setup.from_json(setup_json)
        else:
            raise Exception(message)

class Setup(object):
    @classmethod
    def from_json(cls, js):

        obj = object.__new__(cls)
        obj._js = js
        obj.parts = [Part.from_json(part_js) for part_js in json.loads(js['content'])]

        return obj

    @property
    def name(self):
        return self._js['name']

class Part(object):
    @classmethod
    def from_json(cls, js):
        obj = object.__new__(cls)

        obj._js = js
        print(js)
        obj._pose = Pose.from_matrix_elements(js['worldMatrix']['elements'])

        return obj

    def get_label(self):
        return self._js['label']['label']

    def set_label(self, value):
        self._js['label']['label'] = value

    label = property(get_label, set_label)

    @property
    def pose(self):
        return self._pose

class Pose(object):
    @classmethod
    def from_matrix_elements(cls, matrix_elements):
        obj = object.__new__(cls)

        obj._matrix_elements = matrix_elements
        obj._position = Position.from_matrix_elements(matrix_elements)
        obj._rotation = Rotation.from_matrix_elements(matrix_elements)

        return obj

    @property
    def position(self):
        return self._position

    @property
    def rotation(self):
        return self._rotation

class Position(object):
    @classmethod
    def from_matrix_elements(cls, matrix_elements):
        obj = object.__new__(cls)

        obj._matrix_elements = matrix_elements

        return obj

    def get_x(self):
        return self._matrix_elements[12]

    def set_x(self, value):
        self._matrix_elements[12] = value

    def get_y(self):
        return self._matrix_elements[13]

    def set_y(self, value):
        self._matrix_elements[13] = value

    def get_z(self):
        return self._matrix_elements[14]

    def set_z(self, value):
        self._matrix_elements[14] = value

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)

class Rotation(object):
    @classmethod
    def from_matrix_elements(cls, matrix_elements):
        obj = object.__new__(cls)

        obj._matrix_elements = matrix_elements
        obj._x, obj._y, obj._z = obj.rotation_angles()

        return obj

    def update_matrix_elements(self):
        cx, sx = math.cos(self._x), math.sin(self._x)
        cy, sy = math.cos(self._y), math.sin(self._y)
        cz, sz = math.cos(self._z), math.sin(self._z)

        self._matrix_elements[0]  =  cy*cz
        self._matrix_elements[1]  = -cy*sz
        self._matrix_elements[2]  =  sy

        self._matrix_elements[4]  =  cx*sz + cz*sx*sy
        self._matrix_elements[5]  =  cx*cz - sx*sy*sz
        self._matrix_elements[6]  = -cy*sx

        self._matrix_elements[8]  =  sx*sz - cx*cz*sy
        self._matrix_elements[9]  =  cz*sx + cx*sy*sz
        self._matrix_elements[10] =  cx*cy

    def rotation_angles(self):
        r11, r12, r13 = self._matrix_elements[0], self._matrix_elements[1], self._matrix_elements[2]
        r21, r22, r23 = self._matrix_elements[4], self._matrix_elements[5], self._matrix_elements[6]
        r31, r32, r33 = self._matrix_elements[8], self._matrix_elements[9], self._matrix_elements[10]

        x = math.atan(r23/r33)
        y = math.atan(-r13*math.cos(x)/r33)
        z = math.atan(r12/r11)

        return [x, y, z]

    def get_x(self):
        return self._x

    def set_x(self, value):
        self._x = value
        self.update_matrix_elements()

    def get_y(self):
        return self._y

    def set_y(self, value):
        self._y = value
        self.update_matrix_elements()

    def get_z(self):
        return self._z

    def set_z(self, value):
        self._z = value
        self.update_matrix_elements()

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)

def healthcheck():
    url = API_URL + 'healthcheck'
    r = requests.get(url).json()
    return (r['status'] == 'SUCCESS', r['message'])

def get(endpoint, api_key):
    url = API_URL + endpoint
    headers = {'X-API-KEY': api_key}
    r = requests.get(url, headers=headers).json()
    return (r['data'] if 'status' in r and r['status'] == 'SUCCESS' else None, r['message'])

def get_setups(api_key):
    return get('setups', api_key)

def get_setup(setup_id, api_key):
    return get(f'setups/{setup_id}', api_key)
