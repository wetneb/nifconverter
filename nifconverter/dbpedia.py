import requests
from .uriconverter import URIConverter

class FromDBpediaConverter(URIConverter):
    batch_size = 20
    dbpedia_prefix = 'http://dbpedia.org/resource/'

    def __init__(self, target_prefix='http://en.wikipedia.org/wiki/'):
        """
        Creates a converter from DBpedia to one of the other URI schemes
        DBpedia knows of via owl:sameAs.

        The target prefix is used to select these links.
        """
        self.target_prefix = target_prefix

    def is_convertible(self, uri):
        return uri.startswith(self.dbpedia_prefix)

    def convert(self, uris):
        """
        This uses DBpedia's SPARQL endpoint to convert the identifiers.
        """
        uris = [uri.replace(' ','_') for uri in uris]

        sparql_query = """
        SELECT ?uri ?dbp WHERE {{
           ?dbp owl:sameAs ?uri.
           VALUES ?dbp {{ {uris} }}
        }}
        """.format(uris=' '.join('<{}>'.format(uri) for uri in uris))

        r = requests.get('http://dbpedia.org/sparql/', {'query':sparql_query, 'format':'json'})
        r.raise_for_status()
        results = r.json()['results']

        mapping = {}
        for binding in results['bindings']:
            dbp = binding['dbp']['value']
            uri = binding['uri']['value']
            if uri.startswith(self.target_prefix):
                mapping[dbp] = uri

        return mapping

class ToDBpediaConverter(URIConverter):
    batch_size = 20
    dbpedia_prefix = 'http://dbpedia.org/resource/'

    def __init__(self, source_prefix='http://www.wikidata.org/entity/'):
        """
        Creates a converter to DBpedia to one of the other URI schemes
        DBpedia knows of via owl:sameAs.

        The source prefix is used to select these links.
        """
        self.source_prefix = source_prefix

    def is_convertible(self, uri):
        return uri.startswith(self.source_prefix)

    def convert(self, uris):
        """
        This uses DBpedia's SPARQL endpoint to convert the identifiers.
        """
        uris = [uri.replace(' ','_') for uri in uris]

        sparql_query = """
        SELECT ?uri ?dbp WHERE {{
           ?dbp owl:sameAs ?uri.
           VALUES ?uri {{ {uris} }}
        }}
        """.format(uris=' '.join('<{}>'.format(uri) for uri in uris))

        r = requests.get('http://dbpedia.org/sparql/', {'query':sparql_query, 'format':'json'})
        r.raise_for_status()
        results = r.json()['results']

        mapping = {}
        for binding in results['bindings']:
            dbp = binding['dbp']['value']
            uri = binding['uri']['value']
            if uri.startswith(self.source_prefix):
                mapping[uri] = dbp

        return mapping


