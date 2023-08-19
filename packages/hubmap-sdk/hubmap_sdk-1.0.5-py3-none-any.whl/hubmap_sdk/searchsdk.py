import requests

from hubmap_sdk import sdk_helper


class SearchSdk:

    def __init__(self, token=None, service_url="https://search.api.hubmapconsortium.org/"):
        self.header = {}
        self.token = token
        if service_url.endswith('/'):
            self.search_url = service_url
        else:
            self.search_url = service_url + '/'
        if token is not None:
            self.header['Authorization'] = f'Bearer {self.token}'

    def assaytype(self, key):
        url = f"{self.search_url}assaytype"
        key = f"?{key}"
        output = sdk_helper.make_request('get', self, url, optional_argument=key)
        return output

    def assayname(self, name):
        url = f"{self.search_url}assaytype/{name}"
        output = sdk_helper.make_request('get', self, url)
        return output

    def search(self, data):
        url = f"{self.search_url}search"
        output = sdk_helper.make_request('post', self, url, data=data)
        return output

    def search_by_index(self, data, index_without_prefix):
        url = f"{self.search_url}{index_without_prefix}/search"
        output = sdk_helper.make_request('post', self, url, data=data)
        return output


    def count(self, data):
        url = f"{self.search_url}count"
        output = sdk_helper.make_request('get', self, url, data=data)
        return output

    def count_by_index(self, data, index_without_prefix):
        url = f"{self.search_url}{index_without_prefix}/count"
        output = sdk_helper.make_request('get', self, url, data=data)
        return output

    def indices(self):
        url = f"{self.search_url}indices"
        output = sdk_helper.make_request('get', self, url)
        indices = output['indices']
        return indices

    def status(self):
        try:
            r = requests.get(self.search_url + 'status')
        except Exception as e:
            print(e)
            return e
        output = r.json()
        if r.status_code < 300:
            print(f"build: {output['build']}, elasticsearch_connection: {output['elasticsearch_connection']}, "
                  f"elasticsearch_status: {output['elasticsearch_status']}, version: {output['version']}")
        return output
    def reindex(self, uuid):
        url = f"{self.search_url}reindex/{uuid}"
        output = sdk_helper.make_request('put', self, url)
        return output, 202

    def reindex_all(self):
        url = f"{self.search_url}reindex-all"
        output = sdk_helper.make_request('put', self, url)
        return output, 202
