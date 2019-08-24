# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

from .uriconverter import URIConverter
from .utils import retry_request, fetch_redirecting_uris, DBPEDIA_PREFIX, DBPEDIA_PAGE_PREFIX


class FromDBpediaSparqlConverter(URIConverter):
    batch_size = 20

    def __init__(self, target_prefix='http://en.wikipedia.org/wiki/'):
        """
        Creates a converter from DBpedia to one of the other URI schemes
        DBpedia knows of via owl:sameAs.

        The target prefix is used to select these links.
        """
        super(FromDBpediaSparqlConverter, self).__init__(target_prefix)

    def is_convertible(self, uri):
        return uri.startswith(DBPEDIA_PREFIX) or uri.startswith(DBPEDIA_PAGE_PREFIX)

    def convert(self, uris):
        """
        This uses DBpedia's SPARQL endpoint to convert the identifiers.
        """
        decoded_uris = {
            uri: unquote(uri).replace(' ', '_').replace('"', '%22').replace(DBPEDIA_PAGE_PREFIX, DBPEDIA_PREFIX)
            for uri in uris
        }

        sparql_query = """
        SELECT ?source ?target WHERE {{
           ?source owl:sameAs ?target .
           VALUES ?source {{ {uris} }}
        }}
        """.format(uris=' '.join({'<{}>'.format(uri) for uri in decoded_uris.values()}))

        mapping = fetch_mapping(sparql_query, self.target_prefix)

        # Additionally, try to resolve redirected resources
        redirecting_uris = fetch_redirecting_uris(decoded_uris.values(), mapping.keys())
        if redirecting_uris:
            redirect_mapping = self.convert(redirecting_uris.values())
            mapping.update({
                decoded_uri: redirect_mapping[redirected_uri]
                for decoded_uri, redirected_uri in redirecting_uris.items()
                if redirected_uri in redirect_mapping
            })

        return {
            uri: mapping[decoded_uri]
            for uri, decoded_uri in decoded_uris.items()
            if decoded_uri in mapping
        }


class ToDBpediaSparqlConverter(URIConverter):
    batch_size = 20

    def __init__(self, target_prefix=DBPEDIA_PREFIX):
        """
        Creates a converter to DBpedia to one of the other URI schemes
        DBpedia knows of via owl:sameAs.
        """
        super(ToDBpediaSparqlConverter, self).__init__(DBPEDIA_PREFIX)
        if target_prefix != DBPEDIA_PREFIX:
            raise ValueError('ToDBpediaSparqlConverter only supports converting to DBpedia URIs, starting with '+DBPEDIA_PREFIX)

    def is_convertible(self, uri):
        # TODO: find out which namespaces are available from the SPARQL interface
        return True

    def convert(self, uris):
        """
        This uses DBpedia's SPARQL endpoint to convert the identifiers.
        """
        uris = [uri.replace(' ', '_').replace('"', '%22') for uri in uris]

        sparql_query = """
        SELECT ?source ?target WHERE {{
           ?target owl:sameAs ?source .
           VALUES ?source {{ {uris} }}
        }}
        """.format(uris=' '.join('<{}>'.format(uri) for uri in uris))

        return fetch_mapping(sparql_query, DBPEDIA_PREFIX)


def fetch_mapping(sparql_query, prefix):
    r = retry_request(
        'http://dbpedia.org/sparql/',
        {
            'query': sparql_query,
            'format': 'json'
        }
    )
    r.raise_for_status()
    results = r.json()['results']

    mapping = {}
    for binding in results['bindings']:
        source = binding['source']['value']
        target = binding['target']['value']
        if target.startswith(prefix):
            mapping[source] = target

    return mapping
