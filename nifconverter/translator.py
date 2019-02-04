

class NIFTranslator(object):
    """
    Takes NIFCollection object and translates
    it using a URI converter.
    """

    def __init__(self, uri_converter):
        self.uri_converter = uri_converter

    def translate_collection(self, collection):
        """
        Given a collection, add the new URIs using the configured converter.
        Set remove_source_uris to True if the original URIs should be replaced (otherwise they are kept).

        The collection is modified in place.
        """
        all_phrase_uris = [phrase.taIdentRef for phrase in self._enumerate_phrases(collection) if phrase.taIdentRef]
        convertible_uris = [uri for uri in all_phrase_uris if self.uri_converter.is_convertible(uri)]

        uri_map = self.uri_converter.convert(convertible_uris)

        for phrase in self._enumerate_phrases(collection):
            if uri_map.get(phrase.taIdentRef):
                phrase.taIdentRef = uri_map[phrase.taIdentRef]

    def _enumerate_phrases(self, collection):
        """
        Enumerates all the phrases in a collection
        """
        for doc in collection.contexts:
            for phrase in doc.phrases:
                yield phrase

