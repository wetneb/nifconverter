nifconverter
============

`Build Status <https://travis-ci.org/wetneb/nifconverter>`__ `Coverage
Status <https://coveralls.io/github/wetneb/nifconverter?branch=master>`__
`PyPI version <https://pypi.org/project/nifconverter/>`__

Utility to translate NIF files across identifier schemes, for instance
between DBpedia and Wikidata.

It can be used both as a Python library or as a CLI utility.

Install it with ``pip install nifconverter``.

Example invocation:

.. code:: bash

   nifconverter -i my_dbpedia_nif_file.ttl -o my_wikidata_nif_file.ttl

By default we use the `DBpedia SameThing
service <http://dev.dbpedia.org/Global_IRI_Resolution_Service>`__ to
convert URIs. It is also possible to query the DBpedia SPARQL endpoint
instead using the ``--converter`` parameter:

.. code:: bash

   nifconverter --converter FromDBpediaSparqlConverter -i my_dbpedia_nif_file.ttl -o my_wikidata_nif_file.ttl

The target URI space to convert to can be changed with the ``--target``
option:

.. code:: bash

   nifconverter --target https://en.wikipedia.org/wiki/ -i my_wikidata_nif_file.ttl -o my_wikipedia_nif_file.ttl
