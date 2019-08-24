# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from nifconverter.dbpedia_sparql import FromDBpediaSparqlConverter
from nifconverter.dbpedia_sparql import ToDBpediaSparqlConverter
from nifconverter.tests.dbpedia_bases import DBpediaTestBase


class FromDBpediaSparqlConverterTest(DBpediaTestBase.FromDBpediaBase):
    @classmethod
    def setUpClass(cls):
        cls.converter = FromDBpediaSparqlConverter('http://www.wikidata.org/entity/')


class ToDBpediaSparqlConverterTest(DBpediaTestBase.ToDBpediaBase):

    @classmethod
    def setUpClass(cls):
        cls.converter = ToDBpediaSparqlConverter('http://www.wikidata.org/entity/')
