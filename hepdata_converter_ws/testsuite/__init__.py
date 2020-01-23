# -*- encoding: utf-8 -*-
import base64
import tarfile
from io import StringIO
from hepdata_converter.testsuite import _parse_path_arguments, construct_testdata_path

__author__ = 'Michał Szostak'


class insert_data_as_tar_base64(object):
    def __init__(self, *sample_file_name, **kwargs):
        self.sample_file_name = _parse_path_arguments(sample_file_name)
        self.arcname = kwargs.get('arcname', 'hepdata-converter-ws-data')

    def __call__(self, function):
        def _inner(*args, **kwargs):
            data_stream = StringIO()
            with tarfile.open(mode='w:gz', fileobj=data_stream) as data:
                data.add(construct_testdata_path(self.sample_file_name), arcname=self.arcname)

            args = list(args)
            args.append(base64.b64encode(data_stream.getvalue()))
            function(*args, **kwargs)

        return _inner


class insert_data_as_tar(object):
    def __init__(self, *sample_file_name, **kwargs):
        self.sample_file_name = _parse_path_arguments(sample_file_name)
        self.arcname = kwargs.get('arcname', 'hepdata-converter-ws-data')

    def __call__(self, function):
        def _inner(*args, **kwargs):
            data_stream = StringIO()
            with tarfile.open(mode='w:gz', fileobj=data_stream) as data:
                data.add(construct_testdata_path(self.sample_file_name), arcname=self.arcname)

            args = list(args)
            args.append(data_stream.getvalue())
            function(*args, **kwargs)

        return _inner
