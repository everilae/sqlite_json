sqlite_json
===========

Usage
-----

If using SQLAlchemy 1.2.3 or above

.. code:: python

    >>> engine = create_engine("sqlite:///", plugins=["jsonplugin"])

else

.. code:: python

    >>> engine = create_engine("sqlite:///?plugin=jsonplugin")

Because of the way how json1_ extension's `JSON_EXTRACT()` works models have to
use the `JSON` type provided by this package:

.. code:: python

    from sqlite_json import JSON

    class MyModel(Base):
        ...
        data = Column(JSON)

License
-------

This package is licensed under the OSI MIT License.

.. _json1: https://www.sqlite.org/json1.html
