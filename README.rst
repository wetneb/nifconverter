nifconverter
============

`Build Status <https://travis-ci.org/wetneb/nifconverter>`__ `Coverage
Status <https://coveralls.io/github/wetneb/nifconverter?branch=master>`__

Utility to translate NIF files across identifier schemes, for instance
between DBpedia and Wikidata.

It can be used both as a Python library or as a CLI utility.

Example invocation:

.. code:: bash

   nifconverter --mode dbr:wd -i my_dbpedia_nif_file.ttl -o my_wikidata_nif_file.ttl
