# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
from nifconverter.uriconverter import URIConverter

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


class DBpediaTestBase:
    # class nesting prevents the test runner from picking up bases

    class FromDBpediaBase(unittest.TestCase):

        @classmethod
        def setUpClass(cls):
            cls.converter = URIConverter()

        def test_is_convertible(self):
            self.assertTrue(self.converter.is_convertible('http://dbpedia.org/resource/Douglas_Adams'))
            self.assertFalse(self.converter.is_convertible('http://en.wikipedia.org/wiki/Douglas_Adams'))
            self.assertTrue(self.converter.is_convertible('http://dbpedia.org/page/Nebraska_Cornhuskers_football'))

        def test_to_wikidata(self):
            expected_mapping = {
                # Simple case
                'http://dbpedia.org/resource/Douglas_Adams': 'http://www.wikidata.org/entity/Q42',
                # With alternate prefix
                'http://dbpedia.org/page/Nebraska_Cornhuskers_football':'http://www.wikidata.org/entity/Q6984693',
                # For escaping
                'http://dbpedia.org/resource/Fran%C3%A7ois_Legault': 'http://www.wikidata.org/entity/Q3085147',
                # Without escaping, with unicode character
                'http://dbpedia.org/resource/François_Legault': 'http://www.wikidata.org/entity/Q3085147',
                # Without escaping, with quotes
                'http://dbpedia.org/page/Toys_%22R%22_Us': 'http://www.wikidata.org/entity/Q696334',
                # With redirect
                'http://dbpedia.org/resource/Gio_Gonzalez': 'http://www.wikidata.org/entity/Q1525217',
            }
            mapping = self.converter.convert(expected_mapping.keys())
            self.assertEqual(expected_mapping, mapping)

    class ToDBpediaBase(unittest.TestCase):

        @classmethod
        def setUpClass(cls):
            cls.converter = URIConverter()

        def test_is_convertible(self):
            self.assertTrue(self.converter.is_convertible('http://www.wikidata.org/entity/Q42'))

        def test_from_wikidata(self):
            mapping = self.converter.convert([
                'http://www.wikidata.org/entity/Q42',
                'http://www.wikidata.org/entity/Q34433'
            ])
            expected_mapping = {
               'http://www.wikidata.org/entity/Q34433': 'http://dbpedia.org/resource/University_of_Oxford',
               'http://www.wikidata.org/entity/Q42': 'http://dbpedia.org/resource/Douglas_Adams',
            }
            self.assertEqual(expected_mapping, mapping)
