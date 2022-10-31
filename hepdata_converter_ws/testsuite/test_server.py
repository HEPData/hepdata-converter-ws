# -*- encoding: utf-8 -*-
from io import BytesIO
from distlib._backport import tarfile
import os
import tarfile
from flask import jsonify, json
from hepdata_converter.testsuite import insert_data_as_str, insert_path, TMPDirMixin, ExtendedTestCase

import hepdata_converter_ws
import unittest
from hepdata_converter_ws.testsuite import insert_data_as_tar_base64, insert_data_as_tar

__author__ = 'Michał Szostak'


class HepdataConverterWSTestCase(TMPDirMixin, ExtendedTestCase):
    def setUp(self):
        super(HepdataConverterWSTestCase, self).setUp()
        self.app = hepdata_converter_ws.create_app()
        self.app.config['TESTING'] = True
        self.app_client = self.app.test_client()

    def tearDown(self):
        super(HepdataConverterWSTestCase, self).tearDown()


    def assertMultiLineAlmostEqual(self, first, second, msg=None):
        if hasattr(first, 'readlines'):
            lines = first.readlines()
        elif isinstance(first, str):
            lines = first.split('\n')

        if hasattr(second, 'readlines'):
            orig_lines = second.readlines()
        elif isinstance(second, str):
            orig_lines = second.split('\n')

        # Remove blank lines at end of files
        while lines[-1].strip() == '':
            lines.pop()

        while orig_lines[-1].strip() == '':
            orig_lines.pop()

        self.assertEqual(len(lines), len(orig_lines))
        for i in range(len(lines)):
            self.assertEqual(lines[i].strip(), orig_lines[i].strip())


    @insert_data_as_tar_base64('oldhepdata/sample.input')
    @insert_path('oldhepdata/yaml')
    def test_convert(self, hepdata_input_tar, yaml_path):
        r = self.app_client.get('/convert', data=json.dumps({'input': hepdata_input_tar.decode('utf-8'),
                                                      'options': {'input_format': 'oldhepdata', 'output_format': 'yaml'}}),
                         headers={'content-type': 'application/json'})

        with tarfile.open(mode='r:gz', fileobj=BytesIO(r.data)) as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, path=self.current_tmp)

        self.assertDirsEqual(os.path.join(self.current_tmp, 'hepdata-converter-ws-data'), yaml_path)


    @insert_data_as_tar_base64('yaml_full')
    @insert_data_as_str('csv/table_1.csv')
    @insert_path('yaml_full')
    def test_convert_yaml_v0(self, hepdata_input_tar, csv_content, yaml_path):
        r = self.app_client.get(
            '/convert',
            data=json.dumps({
                'input': hepdata_input_tar.decode('utf-8'),
                'options': {
                    'input_format': 'yaml',
                    'output_format': 'csv',
                    'table': 'Table 1',
                    'pack': True,
                    'validator_schema_version': '0.1.0'
                }
            }),
            headers={'content-type': 'application/json'})

        with tarfile.open(mode='r:gz', fileobj=BytesIO(r.data)) as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, path=self.current_tmp)

        self.assertEqual(len(os.listdir(self.current_tmp)), 1)
        output_file_path = os.path.join(self.current_tmp, os.listdir(self.current_tmp)[0])

        with open(output_file_path, 'r') as f:
            self.assertMultiLineAlmostEqual(f, csv_content)


    @insert_data_as_tar_base64('yaml_full')
    @insert_data_as_str('csv/table_1.csv')
    @insert_path('yaml_full')
    def test_convert_yaml_invalid_v1(self, hepdata_input_tar, csv_content, yaml_path):
        with self.assertRaises(RuntimeError) as e:
            r = self.app_client.get(
                '/convert',
                data=json.dumps({
                    'input': hepdata_input_tar.decode('utf-8'),
                    'options': {
                        'input_format': 'yaml',
                        'output_format': 'csv',
                        'table': 'Table 1',
                        'pack': True,
                        'validator_schema_version': '1.0.0'
                    }
                }),
                headers={'content-type': 'application/json'})

        self.assertTrue("did not pass validation" in str(e.exception))

    def test_ping(self):
        r = self.app_client.get('/ping')
        self.assertTrue("OK" in str(r.data))

    def test_debug_sentry(self):
        with self.assertRaises(Exception) as e:
            r = self.app_client.get('/debug-sentry')

        self.assertTrue(str(e.exception) == "Testing that Sentry picks up this error")
