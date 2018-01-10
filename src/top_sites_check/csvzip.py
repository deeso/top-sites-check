from zipfile import ZipFile
import io
from io import StringIO
from urllib import request
import csv
from .interface import ServiceInterface


class CsvZipServiceInterface(ServiceInterface):
    TYPE = "csv-zip"

    @classmethod
    def key(cls):
        return cls.TYPE.lower()

    def __init__(self, name, url=None, filename=None, **kargs):
        super(ServiceInterface, self).__init__(**kargs)
        self.url = url
        self.filename = filename
        self.loaded = False
        self.name = name
        self.update_url = url

        self.data = {}
        self.name_data = {}

    def update(self, **kargs):
        if self.update_url is not None:
            r = request.urlopen(self.update_url)
            self.load_from_file(r)
            return True
        return False

    def load_from_url(self):
        if self.url is not None:
            r = request.urlopen(self.url)
            return self.load_from_file(r)
        return self.name_data

    def load_from_filename(self):
        if self.filename is not None:
            r = open(self.filename)
            return self.load_from_file(r)
        return self.name_data

    def load_from_file(self, file_obj):
        raw_zip_bytes = file_obj.read()
        zip_bytes = io.BytesIO(raw_zip_bytes)
        zf = ZipFile(zip_bytes)
        names = zf.namelist()

        for name in names:
            if name not in self.name_data:
                self.name_data[name] = {}

        for name in names:
            raw_str_data = str(zf.read(name).decode('utf-8')).splitlines()
            raw_csv_data = StringIO("\n".join(raw_str_data))
            rows = [row for row in csv.reader(raw_csv_data)]
            self.name_data[name] = dict([(d, r) for r, d in rows])
        return self.name_data

    def load(self, **kargs):
        if self.filename is not None:
            self.load_from_filename()
            self.loaded = True
        elif self.url is not None:
            self.load_from_url()
            self.loaded = True
        return self.name_data

    def check(self, domain, **kargs):
        for name, info_dict in self.name_data.items():
            if domain in info_dict:
                return {"name": self.name, "rank": info_dict[domain]}
        return {}

    @classmethod
    def parse_toml(cls, toml_dict):
        bt = toml_dict.get('type', None)
        if bt is None or bt != cls.key():
            raise Exception('Attempting to parse the wrong block type')
        name = toml_dict.get('name', 'unknown')
        filename = toml_dict.get('filename', None)
        url = toml_dict.get('url', None)

        if url is None and filename is None:
            raise Exception('Must specify a valid source')

        return cls(name, url=url, filename=filename)
