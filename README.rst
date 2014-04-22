lychee.json
===========

``lychee.json`` is an extreamly fast json encoder / decoder package for python. Encoding and decoding output
fully compatible with ``python.json`` package.

Features
--------

*  Extreamly fast *(see benchmark results in '/test/benchmark' directory)*
*  Fully compatible output with Python json package
*  Builtin object serialization method ``__json__`` *(see below)*
*  Strict `JSON (RFC 4627) <http://www.ietf.org/rfc/rfc4627.txt?number=4627>`_ expected: ``Infinity``, ``NaN`` (*JavaScript* compatible infinity and not a number symbols)
*  UTF-8 encoding / decoding support
*  Accurate float encoding / decoding

Installation
------------

You can install via pip::
   
   pip install lychee.json
   
or setuptools::

   easy_install lychee.json
   

Requirements
^^^^^^^^^^^^

Python 2.6-2.7 developer headers and any ``c`` or ``c++`` compatible compiler, but only tested with gcc under linux.

.. note:: working on py3k compatibility


Usage
-----

Very similar that ``python.json``, let's see some example

Json data to python
   code::
      
      from lychee import json
      
      >>> json.loads('"Hello World"')
      "Hello World"
      
Python object to json data
   code::
   
      from lychee import json
      
      >>> json.dumps("Hello World")
      '"Hello World"'
      
      class Point:
         def __json__(self):
            return {"x":1, "y":2}
      
      >>> json.dumps(Point())
      '{"x":1,"y":2}'

Functions
---------

- **lychee.json.loads** (*str* **s** [, *callable* **object_hook** [, *callable* **parse_float**]])

   * **s**: json string
   * **object_hook**: this function call on every object that decoded example::
      
      >>> from lychee import json      
      >>> def hook(dict_):
      ...     if "__complex__" in dict_:
      ...         return complex(dict_["real"], dict_["imag"])      
      ...
      >>> json.loads('{"__complex__":true, "real":1, "imag":2}', 
      >>>     object_hook=hook)
      (1+2j)

   * **parse_float**: call this function when float parsed from json data. If you are need to use ``decimal.Decimal``
     for float decoding provide this paramater with ``decimal.Decimal`` eg.::
      
      >>> from lychee import json
      >>> from decimal import Decimal
      >>> json.loads("1.2", parse_float=Decimal)
      Decimal('1.2')

- **lychee.json.dumps** (*object* **obj** [, *callable* **default** [, *str* **tojson** [, *bool* **ensure_ascii** [, *bool* **dump_date** [, *int* **utc_offset**]]]]])

   * **obj**: python object
   * **default**: default function for non basic python type serialization::
   
      >>> from lychee import json
      >>> def default_func(o):
      ...     if isinstance(o, complex):
      ...         return {"__complex__":True, "real":1, "imag":2}
      ...
      >>> json.dumps(1 + 2j, default=default_func)
      '{"__complex__":true,"real":1,"imag":2}'
   
   * **tojson**: method name to use to convert object to json serializable type
     when need to serialize non supported object, default value is ``__json__``::
   
      >>> from lychee import json
      >>> class Point(object):
      ...     def __init__(self, x, y):
      ...         self.x = x
      ...         self.y = y
      ...     def __json__(self):
      ...         return {"x":self.x, "y":self.y}
      ...
      >>> json.dumps(Point(10, 20))
      '{"x":10,"y":20}'
   
   * **ensure_ascii**: ancode all characters are ascii compatible format
   
   * **dump_date**: default value is *True*, if *True* automatically convert date / datetime objects to
     `ISO 8601 <http://en.wikipedia.org/wiki/ISO_8601>`_ format.
     
   * **utc_offset**: If *datetime* object has no `tzinfo <http://docs.python.org/2/library/datetime.html#datetime.datetime.tzinfo>`_
     this value is use insted. Possible values is:
     
       a) 'local' string: use machine local utc offset
       b) `timedelta <http://docs.python.org/2/library/datetime.html?highlight=timedelta#datetime.timedelta>`_
       c) int: utc offset in seconds 
     

Exceptions
----------

- ``lychee.json.JsonError``: base exception class
- ``lychee.json.JsonEncodeError``: exception class for encoding errors
- ``lychee.json.JsonDecodeError``: exception class for decoding errors
 
