# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from nifconverter.dbpedia_samething import SameThingConverter
from nifconverter.tests.dbpedia_bases import DBpediaTestBase


class FromDBpSameThingConverterTest(DBpediaTestBase.FromDBpediaBase):
    @classmethod
    def setUpClass(cls):
        cls.converter = SameThingConverter('http://www.wikidata.org/entity/')


class ToDBpSameThingConverterTest(DBpediaTestBase.ToDBpediaBase):
    @classmethod
    def setUpClass(cls):
        cls.converter = SameThingConverter('http://dbpedia.org/resource/')


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

