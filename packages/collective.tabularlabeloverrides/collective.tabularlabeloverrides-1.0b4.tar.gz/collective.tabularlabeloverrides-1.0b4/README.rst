.. This README is meant for consumption by humans and PyPI. PyPI can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on PyPI or github. It is a comment.

.. image:: https://github.com/collective/collective.tabularlabeloverrides/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/collective.tabularlabeloverrides/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/collective.tabularlabeloverrides/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/collective.tabularlabeloverrides?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/collective.tabularlabeloverrides/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/collective.tabularlabeloverrides

.. image:: https://img.shields.io/pypi/v/collective.tabularlabeloverrides.svg
    :target: https://pypi.python.org/pypi/collective.tabularlabeloverrides/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/collective.tabularlabeloverrides.svg
    :target: https://pypi.python.org/pypi/collective.tabularlabeloverrides
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/collective.tabularlabeloverrides.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/collective.tabularlabeloverrides.svg
    :target: https://pypi.python.org/pypi/collective.tabularlabeloverrides/
    :alt: License


================================
collective.tabularlabeloverrides
================================

Allows to override the labels for the tabular view on a Collection.

Features
--------

- provides a behavior for Collections with a Label Overrides field
- These labels will override existing labels in the tabular view
- this addon depends on collective.taxonomy to allow both working together



Installation
------------

Install collective.tabularlabeloverrides by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.tabularlabeloverrides


and then running ``bin/buildout``

Or install it via ``pip install collective.tabularlabeloverrides``


Usage
-----

- Define some label overrides mappings on a Collection
- change the display view to the new ``Tabular label override view``



Authors
-------

Maik Derstappen - md@derico.de


Contributors
------------

Put your name here, you deserve it!

- ?


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.tabularlabeloverrides/issues
- Source Code: https://github.com/collective/collective.tabularlabeloverrides
- Documentation: https://docs.plone.org/foo/bar


Support
-------

If you are having issues, please let us know by opening an issue on GitHub.


License
-------

The project is licensed under the GPLv2.
