# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nifconverter.dbpedia_sparql import FromDBpediaConverter
from nifconverter.dbpedia_sparql import ToDBpediaConverter
from nifconverter.tests.dbpedia_bases import DBpediaTestBase


class FromDBpediaConverterTest(DBpediaTestBase.FromDBpediaBase):
    @classmethod
    def setUpClass(cls):
        cls.converter = FromDBpediaConverter('http://www.wikidata.org/entity/')


class ToDBpediaConverterTest(DBpediaTestBase.ToDBpediaBase):

    @classmethod
    def setUpClass(cls):
        cls.converter = ToDBpediaConverter('http://www.wikidata.org/entity/')
