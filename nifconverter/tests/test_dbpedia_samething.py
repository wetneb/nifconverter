# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

import pytest
import requests_mock
from requests import HTTPError

from nifconverter.dbpedia_samething import SameThingConverter
from nifconverter.settings import SAME_THING_SERVICE_URL
from nifconverter.tests.dbpedia_bases import DBpediaTestBase


class FromDBpSameThingConverterTest(DBpediaTestBase.FromDBpediaBase):
    @classmethod
    def setUpClass(cls):
        cls.converter = SameThingConverter('http://www.wikidata.org/entity/')


class ToDBpSameThingConverterTest(DBpediaTestBase.ToDBpediaBase):
    unconvertible_uris = [
        'mock://not.an.URI',
        'mock://bad.domain/surprise',
        'mock://www.wikidata.org/entity/null',
    ]

    @classmethod
    def setUpClass(cls):
        cls.converter = SameThingConverter('http://dbpedia.org/resource/')

    def test_some_uris_unconvertible(self):
        some_bad_uris = self.unconvertible_uris + ['http://www.wikidata.org/entity/Q1985']
        expected_mapping = {'http://www.wikidata.org/entity/Q1985': 'http://dbpedia.org/resource/2000'}
        with requests_mock.Mocker() as req_mocker:
            req_mocker.get('mock://', status_code=404)
            req_mocker.get(SAME_THING_SERVICE_URL, real_http=True)
            mapping = self.converter.convert(some_bad_uris)

        self.assertEqual(expected_mapping, mapping)

    def test_all_uris_unconvertible(self):
        with pytest.raises(HTTPError) as excinfo:
            self.converter.convert(self.unconvertible_uris)

        assert '404' in str(excinfo.value)


class MultilingualDBpSameThingConverterTest(unittest.TestCase):
    source_uri = 'http://www.wikidata.org/entity/Q8087'

    def test_global(self):
        stc = SameThingConverter('https://global.dbpedia.org/id/')
        target_uri = stc.convert_one(self.source_uri)
        self.assertEqual('https://global.dbpedia.org/id/4y9Et', target_uri)

    def test_eo(self):
        stc = SameThingConverter('http://eo.dbpedia.org/resource/')
        target_uri = stc.convert_one(self.source_uri)
        self.assertEqual('http://eo.dbpedia.org/resource/Geometrio', target_uri)

    def test_nn(self):
        stc = SameThingConverter('http://nn.dbpedia.org/resource/')
        target_uri = stc.convert_one(self.source_uri)
        self.assertEqual('http://nn.dbpedia.org/resource/Geometri', target_uri)

    def test_mk(self):
        stc = SameThingConverter('http://mk.dbpedia.org/resource/')
        target_uri = stc.convert_one(self.source_uri)
        self.assertEqual('http://mk.dbpedia.org/resource/Геометрија', target_uri)

    def test_af(self):
        stc = SameThingConverter('http://af.dbpedia.org/resource/')
        target_uri = stc.convert_one(self.source_uri)
        self.assertEqual('http://af.dbpedia.org/resource/Meetkunde', target_uri)

    def test_is(self):
        stc = SameThingConverter('http://is.dbpedia.org/resource/')
        target_uri = stc.convert_one(self.source_uri)
        self.assertEqual('http://is.dbpedia.org/resource/Rúmfræði', target_uri)

