import requests
import data_types

class VecnomClient:
    def __init__(self, base_url):
        self.base_url = base_url

    # def create_init_sync(self, msg):
    #     url = f"{self.base_url}/init"
    #     response = requests.post(url, json=msg)
    #     return response.json()

    def search(self, query):
        url = f"{self.base_url}/search"
        response = requests.post(url, json=query)
        return response.json()