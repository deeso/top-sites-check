from zipfile import ZipFile
import io
from io import StringIO
from urllib import request
import csv


class ServiceInterface(object):

    def __init__(self, **kargs):
        pass

    def update(self, **kargs):
        raise Exception("Not implemented for this class")

    def load(self, **kargs):
        raise Exception("Not implemented for this class")

    def check(self, domain=None, **kargs):
        raise Exception("Not implemented for this class")


def load_from_url(url, name_data={}):
    name_data = {}
    if url is not None:
        raw_zip_bytes = request.urlopen(url).read()
        zip_bytes = io.BytesIO(raw_zip_bytes)
        zf = ZipFile(zip_bytes)
        names = zf.namelist()

        for name in names:
            if name not in name_data:
                name_data[name] = {}

        for name in names:
            raw_str_data = str(zf.read(name).decode('utf-8')).splitlines()
            raw_csv_data = StringIO("\n".join(raw_str_data))
            rows = [row for row in csv.reader(raw_csv_data)]
            name_data[name] = dict([(d, r) for r, d in rows])
    return name_data


def load_from_filename(filename, name_data={}):
    name_data = {}
    if filename is not None:
        raw_zip_bytes = open(filename).read()
        zip_bytes = io.BytesIO(raw_zip_bytes)
        zf = ZipFile(zip_bytes)
        names = zf.namelist()

        for name in names:
            if name not in name_data:
                name_data[name] = {}

        for name in names:
            raw_str_data = str(zf.read(name).decode('utf-8')).splitlines()
            raw_csv_data = StringIO("\n".join(raw_str_data))
            rows = [row for row in csv.reader(raw_csv_data)]
            name_data[name] = dict([(d, r) for r, d in rows])
    return name_data


def load_from_file(self, file_obj, name_data={}):
    raw_zip_bytes = file_obj.read()
    zip_bytes = io.BytesIO(raw_zip_bytes)
    zf = ZipFile(zip_bytes)
    names = zf.namelist()

    for name in names:
        if name not in name_data:
            name_data[name] = {}

    for name in names:
        raw_str_data = str(zf.read(name).decode('utf-8')).splitlines()
        raw_csv_data = StringIO("\n".join(raw_str_data))
        rows = [row for row in csv.reader(raw_csv_data)]
        name_data[name] = dict([(d, r) for r, d in rows])
    return name_data


class CsvZipServiceInterface(ServiceInterface):
    def __init__(self, name, url=None, filename=None, **kargs):
        super(ServiceInterface, self).__init__(**kargs)
        self.url = url
        self.filename = filename
        self.loaded = False
        self.name = name

        self.data = {}
        self.name_data = {}

    def update(self, **kargs):
        self.load()

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
        if self.url is not None:
            self.load_from_url()
        return self.name_data

    def check(self, domain, **kargs):
        for name, info_dict in self.name_data.items():
            if domain in info_dict:
                return {"name": self.name, "rank": info_dict[domain]}
        return {}


class Backend(ServiceInterface):

    def __init__(self, sources=[], **kargs):
            super(ServiceInterface, self).__init__(**kargs)
            self.sources = sources

    def update(self, **kargs):
        for s in self.sources:
            s.update()

    def load(self, **kargs):
        for s in self.sources:
            s.load()

    def check(self, domain, **kargs):
        results = {}
        for s in self.sources:
            results.update(s.check(domain))
