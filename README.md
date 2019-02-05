nifconverter
============

[![Build Status](https://travis-ci.org/wetneb/nifconverter.svg?branch=master)](https://travis-ci.org/wetneb/nifconverter) [![Coverage Status](https://coveralls.io/repos/github/wetneb/nifconverter/badge.svg?branch=master)](https://coveralls.io/github/wetneb/nifconverter?branch=master)

Utility to translate NIF files across identifier schemes, for instance between DBpedia and Wikidata.

It can be used both as a Python library or as a CLI utility.

Example invocation:
```bash
nifconverter --mode dbr:wd -i my_dbpedia_nif_file.ttl -o my_wikidata_nif_file.ttl
```

