nifconverter
============

[![Build Status](https://travis-ci.org/wetneb/nifconverter.svg?branch=master)](https://travis-ci.org/wetneb/nifconverter) [![Coverage Status](https://coveralls.io/repos/github/wetneb/nifconverter/badge.svg?branch=master)](https://coveralls.io/github/wetneb/nifconverter?branch=master) [![PyPI version](https://img.shields.io/pypi/v/nifconverter.svg)](https://pypi.org/project/nifconverter/)

Utility to translate NIF files across identifier schemes, for instance between DBpedia and Wikidata.

It can be used both as a Python library or as a CLI utility.

Install it with `pip install nifconverter`.

Example invocation:
```bash
nifconverter -i my_dbpedia_nif_file.ttl -o my_wikidata_nif_file.ttl
```

By default we use the [DBpedia SameThing service](http://dev.dbpedia.org/Global_IRI_Resolution_Service) to convert URIs.
It is also possible to query the DBpedia SPARQL endpoint instead using the `--converter` parameter:
```bash
nifconverter --converter FromDBpediaSparqlConverter -i my_dbpedia_nif_file.ttl -o my_wikidata_nif_file.ttl
```

The target URI space to convert to can be changed with the `--target` option:
```bash
nifconverter --target https://en.wikipedia.org/wiki/ -i my_wikidata_nif_file.ttl -o my_wikipedia_nif_file.ttl
```
