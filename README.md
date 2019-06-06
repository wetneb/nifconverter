nifconverter
============

[![Build Status](https://travis-ci.org/wetneb/nifconverter.svg?branch=master)](https://travis-ci.org/wetneb/nifconverter) [![Coverage Status](https://coveralls.io/repos/github/wetneb/nifconverter/badge.svg?branch=master)](https://coveralls.io/github/wetneb/nifconverter?branch=master) [![PyPI version](https://img.shields.io/pypi/v/nifconverter.svg)](https://pypi.org/project/nifconverter/)

Utility to translate NIF files across identifier schemes, for instance between DBpedia and Wikidata.

It can be used both as a Python library or as a CLI utility.

Install it with `pip install nifconverter`.

Example invocation:
```bash
nifconverter --mode dbr:wd -i my_dbpedia_nif_file.ttl -o my_wikidata_nif_file.ttl
```

