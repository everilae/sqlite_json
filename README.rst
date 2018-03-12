sqlite_json
===========

This plugin provides support for the SQLite json1_ extension in the form of an
engine plugin and extended `JSON` type.

Install
-------

.. code::

    pip install git+https://github.com/everilae/sqlite_json

Usage
-----

If using SQLAlchemy 1.2.3 or above

.. code:: python

    >>> engine = create_engine("sqlite:///", plugins=["jsonplugin"])

else

.. code:: python

    >>> engine = create_engine("sqlite:///?plugin=jsonplugin")

License
-------

This package is licensed under the OSI MIT License.

.. _json1: https://www.sqlite.org/json1.html
