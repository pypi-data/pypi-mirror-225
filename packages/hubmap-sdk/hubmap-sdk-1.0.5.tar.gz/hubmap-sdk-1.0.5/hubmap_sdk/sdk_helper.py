import json.decoder

import requests
from hubmap_sdk import Donor, Dataset, Sample, Collection, Upload, Publication



def make_entity(output):
    if output['entity_type'].lower() == 'dataset':
        new_instance = Dataset(output)
    if output['entity_type'].lower() == 'donor':
        new_instance = Donor(output)
    if output['entity_type'].lower() == 'sample':
        new_instance = Sample(output)
    if output['entity_type'].lower() == 'collection':
        new_instance = Collection(output)
    if output['entity_type'].lower() == 'upload':
        new_instance = Upload(output)
    if output['entity_type'].lower() == 'publication':
        new_instance = Publication(output)
    return new_instance


def make_request(method_type, instance, url, optional_argument=None, data=None):
    if optional_argument is None:
        optional_argument = ''
    try:
        if data is None:
            if instance.token is None:
                if method_type == 'get':
                    r = requests.get(url + optional_argument)
                if method_type == 'put':
                    r = requests.put(url + optional_argument)
                if method_type == 'post':
                    r = requests.post(url + optional_argument)
                if method_type == 'delete':
                    r = requests.delete(url + optional_argument)

            else:
                if method_type == 'get':
                    r = requests.get(url + optional_argument, headers=instance.header)
                if method_type == 'put':
                    r = requests.put(url + optional_argument, headers=instance.header)
                if method_type == 'post':
                    r = requests.post(url + optional_argument, headers=instance.header)
                if method_type == 'delete':
                    r = requests.delete(url + optional_argument, headers=instance.header)
        else:
            if not isinstance(data, dict):
                raise Exception("Data given must be a dictionary")
            if instance.token is None:
                if method_type == 'get':
                    r = requests.get(url + optional_argument, json=data)
                if method_type == 'put':
                    r = requests.put(url + optional_argument, json=data)
                if method_type == 'post':
                    r = requests.post(url + optional_argument, json=data)
                if method_type == 'delete':
                    r = requests.delete(url + optional_argument, json=data)
            else:
                if method_type == 'get':
                    r = requests.get(url + optional_argument, headers=instance.header, json=data)
                if method_type == 'put':
                    r = requests.put(url + optional_argument, headers=instance.header, json=data)
                if method_type == 'post':
                    r = requests.post(url + optional_argument, headers=instance.header, json=data)
                if method_type == 'delete':
                    r = requests.delete(url + optional_argument, headers=instance.header, json=data)
    except Exception:
        raise HTTPException("Connection Error. Check that service url is correct in instance of Entity Class", 404)
    if r.status_code > 299:
        # if r.status_code == 401:
        #     raise Exception("401 Authorization Required. No Token or Invalid Token Given")
        try:
            error = r.json()['error']
        except KeyError:
            error = r.json()['message']
        except json.decoder.JSONDecodeError:
            if r.text.startswith('<html>'):
                start_index = r.text.find('401')
                end_index = r.text.find('Required') + 8
                error = r.text[start_index:end_index]
            else:
                raise json.decoder.JSONDecodeError
        raise HTTPException(error, r.status_code)
    else:
        try:
            return r.json()
        except json.decoder.JSONDecodeError:
            return r.text


class HTTPException(Exception):

    def __init__(self, description, status_code):
        Exception.__init__(self, description)
        self.status_code = status_code
        self.description = description

    def get_status_code(self):
        return self.status_code

    def get_description(self):
        return self.description

