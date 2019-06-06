# -*- coding: utf-8 -*-
from __future__ import unicode_literals
try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

import requests.exceptions
from .uriconverter import URIConverter
from .utils import retry_request

class FromDBpediaConverter(URIConverter):
    batch_size = 20
    dbpedia_prefix = 'http://dbpedia.org/resource/'
    dbpedia_page_prefix = 'http://dbpedia.org/page/'

    def __init__(self, target_prefix='http://en.wikipedia.org/wiki/'):
        """
        Creates a converter from DBpedia to one of the other URI schemes
        DBpedia knows of via owl:sameAs.

        The target prefix is used to select these links.
        """
        self.target_prefix = target_prefix

    def is_convertible(self, uri):
        return uri.startswith(self.dbpedia_prefix) or uri.startswith(self.dbpedia_page_prefix)

    def convert(self, uris):
        """
        This uses DBpedia's SPARQL endpoint to convert the identifiers.
        """
        decoded_uris = {
            uri:unquote(uri).replace(' ','_').replace('"','%22').replace(self.dbpedia_page_prefix, self.dbpedia_prefix)
            for uri in uris
        }

        sparql_query = """
        SELECT ?uri ?dbp WHERE {{
           ?dbp owl:sameAs ?uri.
           VALUES ?dbp {{ {uris} }}
        }}
        """.format(uris=' '.join({'<{}>'.format(uri) for uri in decoded_uris.values()}))

        r = retry_request('http://dbpedia.org/sparql/', {'query':sparql_query, 'format':'json'})
        r.raise_for_status()
        results = r.json()['results']

        mapping = {}
        for binding in results['bindings']:
            dbp = binding['dbp']['value']
            uri = binding['uri']['value']
            if uri.startswith(self.target_prefix):
                mapping[dbp] = uri

        # Additionally, try to resolve redirected resources
        missing_dbps = set(decoded_uris.values()) - set(mapping.keys())
        redirecting_uris = {}
        for missing_uri in missing_dbps:
            redirect = self._get_redirect(missing_uri.replace(self.dbpedia_prefix, self.dbpedia_page_prefix))
            if redirect:
                redirecting_uris[missing_uri] = redirect

        if redirecting_uris:
            redirect_mapping = self.convert(redirecting_uris.values())
            mapping.update({
                decoded_uri:redirect_mapping[redirected_uri]
                for decoded_uri, redirected_uri in redirecting_uris.items()
                if redirected_uri in redirect_mapping
            })

        return {
            uri:mapping[decoded_uri]
            for uri, decoded_uri in decoded_uris.items()
            if decoded_uri in mapping
        }

    def _get_redirect(self, url):
        """
        Checks if a URL redirects to another URL, in
        which case the new URL is returned. Otherwise None is returned.
        """
        # Sadly a HEAD request does not work for obscure encoding reasons...
        # See accompanying test case
        try:
            req = retry_request(url)
        except requests.exceptions.RequestException:
            return
        location = req.url
        if location and location != url:
            return location

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
        uris = [uri.replace(' ','_').replace('"','%22') for uri in uris]

        sparql_query = """
        SELECT ?uri ?dbp WHERE {{
           ?dbp owl:sameAs ?uri.
           VALUES ?uri {{ {uris} }}
        }}
        """.format(uris=' '.join('<{}>'.format(uri) for uri in uris))

        r = retry_request('http://dbpedia.org/sparql/', {'query':sparql_query, 'format':'json'})
        r.raise_for_status()
        results = r.json()['results']

        mapping = {}
        for binding in results['bindings']:
            dbp = binding['dbp']['value']
            uri = binding['uri']['value']
            if uri.startswith(self.source_prefix):
                mapping[uri] = dbp

        return mapping


