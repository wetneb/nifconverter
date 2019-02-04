import os
import unittest
from nifconverter.translator import NIFTranslator
from nifconverter.uriconverter import URIConverter
from pynif import NIFCollection

class DummyURIConverter(URIConverter):
    dbp_prefix = 'http://dbpedia.org/resource/'
    wp_prefix = 'http://en.wikipedia.org/wiki/'

    def is_convertible(self, uri):
        return uri.startswith(self.dbp_prefix)

    def convert_one(self, uri):
        return self.wp_prefix + uri[len(self.dbp_prefix):]

    def convert(self, uris):
        return {uri:self.convert_one(uri) for uri in uris}


class NIFTranslatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        testdir = os.path.dirname(os.path.abspath(__file__))
        cls.dbpedia_nif = NIFCollection.load(os.path.join(testdir, 'data/sample_dbpedia.ttl'))
        cls.wikipedia_nif = NIFCollection.load(os.path.join(testdir, 'data/sample_wikipedia.ttl'))

    def test_translate_collection(self):
        converter = DummyURIConverter()
        translator = NIFTranslator(converter)

        translator.translate_collection(self.dbpedia_nif)

        self.assertEqual(self.wikipedia_nif, self.dbpedia_nif)

