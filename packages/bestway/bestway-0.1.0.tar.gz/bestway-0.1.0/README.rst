bestway
=======

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
