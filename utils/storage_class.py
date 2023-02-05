import os
import requests
from zipfile import ZipFile

from abc import abstractmethod
from io import BytesIO


class Storage:

    @abstractmethod
    def save_zip() -> str:...

    @abstractmethod
    def get_zip() -> BytesIO:...


class DiskStorage(Storage):
    '''Saves zip to disk'''
    def __init__(self, path) -> None:
        self.path = path
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))

    def save_zip(self, zip: ZipFile, filename: str) -> str:
        file_path = os.path.join(os.path.abspath(self.path), filename)
        with open(file_path, 'wb') as file:
            file.write(zip.getbuffer())

        return file_path

    def get_zip(path) -> BytesIO:
        data = None
        with open(path, 'rb') as file:
            data = file.read()

        return data


class CloudStorage(Storage):
    '''Saves zip to transfer.sh service'''
    def __init__(self, url: str) -> None:
        self.url = url

    def save_zip(self, file_name: str, url: str, ttl: int=1) -> str:
        files=[('',(file_name, open(url,'rb'),'application/zip'))]
        headers = {'Max-Days': str(ttl),'Max-Downloads': '1'}
        response = requests.put(url=self.url+file_name, headers=headers, files=files)

        if response.status_code == 200:
            os.remove(url)
            return response.text
        return url

    def get_zip(url) -> BytesIO:
        pass