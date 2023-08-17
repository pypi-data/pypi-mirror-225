.. _dqsegdb2-introduction:

###########
Basic usage
###########

The DQSEGDB service allows users to query for metadata associated
with the operational status of the GEO, KAGRA, LIGO, and Virgo
gravitational-wave detectors.

The ``dqsegdb2`` Python package provides a number of functions to make requests
to a DQSEGDB instance with authorisation credential handling.

.. _dqsegdb2-top-api:

=============
Top-level API
=============

The :mod:`dqsegdb2` top-level module provides the following functions
to perform basic queries against a DQSEGDB instance:

.. currentmodule:: dqsegdb2

.. autosummary::
    :nosignatures:

    query_ifos
    query_names
    query_versions
    query_segments

For example:

.. code-block:: python
    :caption: Query for segments associated with a versioned flag
    :name: dqsegdb2-basic-query_segments

    from dqsegdb2 import query_segments
    print(query_segments('G1:GEO-SCIENCE:1', 1000000000, 1000001000))
