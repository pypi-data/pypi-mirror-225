import requests
import pandas as pd
from typing import Union
import asyncio
import json

API_URL = "https://api.3doptix.com/v1/"

class Setup(object):
    def __init__(self):
        raise TypeError("Cannot create instance of type 'Setup'")

    @classmethod
    def new(cls, id, name, owner):
        obj = object.__new__(cls)
        obj.id = id
        obj.name = name
        obj.owner = owner

        obj.parts = None

        return obj

    def set_from_json(self, json):
        self.parts = []
        for part_json in json[self.id]['parts']:
            self.parts.append(Part.new(part_json['id'], part_json['label'], self))

        return self

    def get_parts(self):
        return self.parts

    def __str__(self):
        return self.name


class ThreedOptixAPI(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def is_up(self):
        return healthcheck()[0]

    def get_setups(self):
        json, message = get_setups(self.api_key)
        if json is not None:
            setups = []
            for setup_json in json['setups']:
                setups.append(Setup.new(setup_json['id'], setup_json['name'], None))
            return setups
        else:
            raise Exception(message)

    def fetch(self, obj):
        if isinstance(obj, Setup):
            self.fetch_setup(obj)
        elif isinstance(obj, Part):
            self.fetch_part(obj)
        elif isinstance(obj, AnalysisResult):
            self.fetch_analysis_result(obj)
        else:
            raise TypeError(f"Cannot fetch instance of type '{obj.__class__.__name__}'")

    def update(self, obj):
        if isinstance(obj, Part):
            self.update_part(obj)
        else:
            raise TypeError(f"Cannot update instance of type '{obj.__class__.__name__}'")

    def run(self, setup):
        data, message = run_simulation(setup.id, self.api_key)
        if data is not None:
            return AnalysisResult.new(data['simulation_result_link'])
        else:
            raise Exception(message)

    def fetch_setup(self, setup):
        json, message = get_setup(setup.id, self.api_key)

        if json is not None:
            setup.set_from_json(json)

        else:
            raise Exception(message)

    def fetch_part(self, part):
        json, message = get_part(part.owner.id, part.id, self.api_key)
        if json is not None:
            part.set_from_json(json)
        else:
            raise Exception(message)

    def fetch_analysis_result(self, result):
        result.data = pd.read_csv(result.url)

    def update_part(self, part):
        success, message = set_part(part.owner.id, part.id, part.to_json(), self.api_key)
        if not success:
            raise Exception(message)


class Part(object):
    def __init__(self):
        raise TypeError("Cannot create 'Part' instances")

    @classmethod
    def new(cls, id, label, owner):
        obj = object.__new__(cls)
        obj.id = id
        obj.label = label
        obj.owner = owner

        obj.pose = None

        return obj

    def set_from_json(self, json):
        json = json[self.id]
        self.pose = Pose().set_from_json(json['pose'])

        return self

    def to_json(self):
        json = {}
        if self.pose is not None:
            json['pose'] = self.pose.to_json()
        return json

    def change_rotation(self, rotation):
        self.pose.rotation = rotation
        return (self.pose.rotation.x, self.pose.rotation.y, self.pose.rotation.z)

    def change_position(self, position):
        self.pose.position.x = position.x
        self.pose.position.y = position.y
        self.pose.position.z = position.z
        return (self.pose.position.x, self.pose.position.y, self.pose.position.z)

    def __str__(self):
        return self.label


class AnalysisResult(object):
    def __init__(self):
        raise TypeError("Cannot create 'AnalysisResult' instances")

    @classmethod
    def new(cls, url):
        obj = object.__new__(cls)
        obj.url = url
        obj.data = None
        return obj


class Vector3(object):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def set_from_json(self, json):
        self.x = json[0]
        self.y = json[1]
        self.z = json[2]

        return self

    def to_json(self):
        return [self.x, self.y, self.z]

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'


class Pose(object):
    def __init__(self, position=Vector3(), rotation=Vector3()):
        self.position = position
        self.rotation = rotation

    def set_from_json(self, json):
        self.position = Vector3().set_from_json(json['position'])
        self.rotation = Vector3().set_from_json(json['rotation'])

        return self

    def to_json(self):
        return {'position': self.position.to_json(), 'rotation': self.rotation.to_json()}

    def __str__(self):
        return f'position={self.position} rotation={self.rotation}'


def healthcheck():
    url = API_URL + 'healthcheck'
    r = requests.get(url).json()
    return (r['status'] == 'SUCCESS', r['message'])

def get(endpoint, api_key):
    url = API_URL + endpoint
    headers = {'X-API-KEY': api_key}
    r = requests.get(url, headers=headers).json()
    return (r['data'] if 'status' in r and r['status'] == 'SUCCESS' else None, r['message'])

def put(endpoint, data, api_key):
    url = API_URL + endpoint
    headers = {'X-API-KEY': api_key}

    r = requests.put(url, headers=headers, json=data)
    return r

def set(endpoint, data, api_key):
    url = API_URL + endpoint
    headers = {'X-API-KEY': api_key}
    r = requests.post(url, headers=headers, json=data).json()
    return ('status' in r and r['status'] == 'SUCCESS', r['message'])

def get_setups(api_key):
    return get('setups', api_key)

def get_setup(setup_id, api_key):
    return get(f'setups/{setup_id}', api_key)

def get_part(setup_id, part_id, api_key):
    return get(f'setups/{setup_id}/parts/{part_id}', api_key)

def set_part(setup_id, part_id, data, api_key):
    return set(f'setups/{setup_id}/parts/{part_id}', data, api_key)

def run_simulation(setup_id, api_key):
    url = API_URL + f'setups/{setup_id}/simulation'
    headers = {'X-API-KEY': api_key}
    r = requests.put(url, headers=headers).json()
    return (r['data'] if 'status' in r and r['status'] == 'SUCCESS' else None, r['message'])
