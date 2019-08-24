

class URIConverter(object):
    """
    Interface for a URI converter.
    """
    batch_size = 1

    def __init__(self, target_prefix):
        """
        Initializes the converter to output URIs with the
        given target prefix.
        Subclasses can throw ValueError if the supplied
        target prefix is not supported.
        """
        self.target_prefix = target_prefix

    def is_convertible(self, uri):
        """
        Is this URI convertible by this converter?
        """
        raise NotImplemented

    def convert_one(self, uri):
        """
        Convert one URI (assumed to be convertible).
        Returns the converted URI or None if the concept does
        not exist in the target domain.
        """
        return self.convert([uri]).get(uri)


    def convert(self, uris):
        """
        Converts a list of URIs, whose length should
        not be greater than batch_size.

        Returns a map of results (from the original uri to the target uri).
        """
        raise NotImplemented

