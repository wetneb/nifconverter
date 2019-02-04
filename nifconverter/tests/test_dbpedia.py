import unittest
from nifconverter.dbpedia import FromDBpediaConverter
from nifconverter.dbpedia import ToDBpediaConverter

class FromDBpediaConverterTest(unittest.TestCase):
    def test_is_convertible(self):
        converter = FromDBpediaConverter('http://www.wikidata.org/entity/')
        self.assertTrue(converter.is_convertible('http://dbpedia.org/resource/Douglas_Adams'))
        self.assertFalse(converter.is_convertible('http://en.wikipedia.org/wiki/Douglas_Adams'))

    def test_to_wikidata(self):
        converter = FromDBpediaConverter('http://www.wikidata.org/entity/')
        mapping = converter.convert(['http://dbpedia.org/resource/University_of_Oxford', 'http://dbpedia.org/resource/Douglas_Adams'])

        expected_mapping = {
            'http://dbpedia.org/resource/University_of_Oxford':'http://www.wikidata.org/entity/Q34433',
            'http://dbpedia.org/resource/Douglas_Adams': 'http://www.wikidata.org/entity/Q42',
        }
        self.assertEqual(expected_mapping, mapping)

class ToDBpediaConverterTest(unittest.TestCase):
    def test_is_convertible(self):
        converter = ToDBpediaConverter('http://www.wikidata.org/entity/')
        self.assertTrue(converter.is_convertible('http://www.wikidata.org/entity/Q42'))
        self.assertFalse(converter.is_convertible('http://en.wikipedia.org/wiki/Douglas_Adams'))

    def test_from_wikidata(self):
        converter = ToDBpediaConverter('http://www.wikidata.org/entity/')
        mapping = converter.convert(['http://www.wikidata.org/entity/Q42', 'http://www.wikidata.org/entity/Q34433'])

        expected_mapping = {
           'http://www.wikidata.org/entity/Q34433': 'http://dbpedia.org/resource/University_of_Oxford',
           'http://www.wikidata.org/entity/Q42': 'http://dbpedia.org/resource/Douglas_Adams',
        }
        self.assertEqual(expected_mapping, mapping)
