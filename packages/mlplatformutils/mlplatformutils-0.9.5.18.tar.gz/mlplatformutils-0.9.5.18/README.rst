MLPlatformUtils Project
===============
This project is used to package all the observability utils for lineage, dependency, telemetry and data read/writes.
Python packages on PyPI.

Installing
============

.. code-block:: bash

    pip install mlplatformutils

Usage
=====

.. code-block:: bash

    >>> from mlplatformutils.core.platformutils import is_package_installed
    >>> print(is_package_installed("pandas"))
