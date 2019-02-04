
import pynif
import sys
from nifconverter.translator import NIFTranslator
from nifconverter.dbpedia import ToDBpediaConverter

if __name__ == '__main__':
    """
    Converts a NIF file with Wikidata ids to a NIF file with DBpedia ids

    Usage: python example.py my_wikidata_nif.ttl my_dbpedia_nif.ttl
    """
    nif = pynif.NIFCollection.load(sys.argv[1])

    translator = NIFTranslator(ToDBpediaConverter())

    translator.translate_collection(nif)

    nif.dump(sys.argv[2])
