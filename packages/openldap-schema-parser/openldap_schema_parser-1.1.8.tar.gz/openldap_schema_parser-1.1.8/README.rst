.. image:: https://img.shields.io/pypi/pyversions/openldap-schema-parser
   :target: https://pypi.org/project/openldap-schema-parser/
   :alt: PyPI - Python Version
.. image:: https://badge.fury.io/py/openldap-schema-parser.svg
   :target: https://pypi.org/project/openldap-schema-parser/
.. image:: https://github.com/mypaceshun/openldap-schema-parser/workflows/Test/badge.svg?branch=main&event=push
   :target: https://github.com/mypaceshun/openldap-schema-parser/actions/workflows/main.yml
.. image:: https://codecov.io/gh/mypaceshun/openldap-schema-parser/branch/main/graph/badge.svg?token=1H6ZVS122O
   :target: https://codecov.io/gh/mypaceshun/openldap-schema-parser
.. image:: https://static.pepy.tech/badge/openldap-schema-parser
   :target: https://www.pepy.tech/projects/openldap-schema-parser
.. image:: https://readthedocs.org/projects/openldap-schema-parser/badge/?version=latest
   :target: https://openldap-schema-parser.readthedocs.io/ja/latest/?badge=latest
   :alt: Documentation Status


openldap-schema-parser
######################

OpenLDAP の schema ファイルをパースします。

Repository
----------

https://github.com/mypaceshun/openldap-schema-parser

Document
--------

https://openldap-schema-parser.readthedocs.io/ja/latest/

Install
-------

::

  $ pip install openldap-schema-parser

Command Usage
-------------

::

  Usage: schema-parser [OPTIONS] TARGET

  Options:
    --version     Show the version and exit.
    -h, --help    Show this message and exit.
    --expand-oid  Expand ObjectIdentifier

Library Usage
-------------

::

  from openldap_schema_parser.parser import parse

  result = parse("test.schema")
  print(result)
