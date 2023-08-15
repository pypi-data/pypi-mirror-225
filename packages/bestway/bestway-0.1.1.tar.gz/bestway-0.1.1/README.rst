bestway 🤸
==========

.. image:: https://github.com/d4v1ncy/bestway/actions/workflows/bestway.yml/badge.svg
   :target: https://github.com/d4v1ncy/bestway/actions/workflows/bestway.yml

.. image:: https://img.shields.io/pypi/dm/bestway
   :target: https://pypi.org/project/bestway

.. image:: https://img.shields.io/pypi/v/bestway
   :target: https://pypi.org/project/bestway

.. image:: https://img.shields.io/pypi/l/bestway?label=PyPi%20License
   :target: https://pypi.org/project/bestway




The best way to craft exit codes: xor'ing a string


Installing
----------

.. code:: bash

    $ pip install bestway

Usage Examples
--------------

.. code:: python

   from bestway import fromstr

   raise SystemExit(fromstr('oops'))

Or in case of emergencies:

.. code:: python

   from bestway import Exit

   raise Exit('error')
