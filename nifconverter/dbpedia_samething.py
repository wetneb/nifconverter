import itertools

from nifconverter.settings import SAME_THING_SERVICE_URL
from nifconverter.uriconverter import URIConverter
from nifconverter.utils import retry_request, fetch_redirecting_uris

try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote


class SameThingConverter(URIConverter):
    """
    URI converter that uses the DBpedia Same Thing Service.
    see http://dev.dbpedia.org/Global_IRI_Resolution_Service
    """
    batch_size = 50

    def __init__(self, target_prefix='http://www.wikidata.org/entity/'):
        super(SameThingConverter, self).__init__(target_prefix)

    def is_convertible(self, uri):
        # todo: https://github.com/dbpedia/dbp-same-thing-service/issues/9
        return any(
            name in uri
            for name in [
                'dbpedia.org',
                'wikidata.org'
            ]
        )

    def convert_one(self, uri):
        """
        Convert one URI (assumed to be convertible).
        Returns the converted URI or None if the concept does
        not exist in the target domain.
        """
        resp = retry_request(
            SAME_THING_SERVICE_URL,
            {
                'meta': 'off',
                'uri': uri
            }
        )
        if resp.status_code == 404:
            # Additionally, try to resolve redirected resources
            redirecting_uris = fetch_redirecting_uris([uri], [None])
            if redirecting_uris:
                return self.convert_one(redirecting_uris[uri])
            else:
                return None

        resp.raise_for_status()
        identifiers = resp.json()
        for target_uri in itertools.chain(
            [identifiers['global']],
            identifiers['locals']
        ):
            if target_uri.startswith(self.target_prefix):
                return target_uri

    def convert(self, uris):
        """
        Converts a list of URIs, whose length should
        not be greater than batch_size.

        Returns a map of results (from the original uri to the target uri).
        """
        resp = retry_request(
            SAME_THING_SERVICE_URL,
            {
                'meta': 'off',
                'uris': uris
            }
        )
        resp.raise_for_status()
        uri_map = resp.json()['uris']
        results = {}

        # try to resolve redirected resources
        redirecting_uris = {}
        if not all(uri_map.values()):
            possible_redirects = [
                source_uri
                for source_uri, identifiers in uri_map.items()
                if not identifiers
            ]
            redirecting_uris = fetch_redirecting_uris(possible_redirects, [None])

        # filter target URIs
        for source_uri, identifiers in uri_map.items():
            if identifiers:
                for target_uri in itertools.chain(
                        [identifiers['global']],
                        identifiers['locals']
                ):
                    if target_uri.startswith(self.target_prefix):
                        results[source_uri] = target_uri
                        break
            elif source_uri in redirecting_uris:
                results[source_uri] = self.convert_one(redirecting_uris[source_uri])

        return results
