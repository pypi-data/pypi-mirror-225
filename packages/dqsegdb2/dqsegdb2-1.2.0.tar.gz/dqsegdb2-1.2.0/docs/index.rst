.. sectionauthor:: Duncan Macleod <duncan.macleod@ligo.org>

.. toctree::
   :hidden:

   DQSEGDB2 <self>

########
DQSEGDB2
########

.. ifconfig:: 'dev' in release

   .. warning::

      You are viewing documentation for a development build of dqsegdb2.
      This version may include unstable code, or breaking changes relative
      the most recent stable release.
      To view the documentation for the latest stable release of dqsegdb2,
      please `click here <../stable/>`_.

.. image:: https://badge.fury.io/py/dqsegdb2.svg
   :target: https://badge.fury.io/py/dqsegdb2
   :alt: dqsegdb2 PyPI release badge
.. image:: https://img.shields.io/pypi/l/dqsegdb2.svg
   :target: https://choosealicense.com/licenses/gpl-3.0/
   :alt: dqsegdb2 license
.. image:: https://zenodo.org/badge/136390328.svg
   :target: https://zenodo.org/badge/latestdoi/136390328
   :alt: dqsegdb2 DOI

``dqsegdb2`` is a Python implementation of the DQSEGDB API as
defined in `LIGO-T1300625 <https://dcc.ligo.org/LIGO-T1300625/public>`__.

.. toctree::
    :caption: Documentation
    :maxdepth: 1

    Installation <install>
    Basic usage <intro>
    Session usage <session>
    Authorisation <auth>

.. toctree::
    :caption: Module documentation
    :maxdepth: 1

    query
    api
    requests
    utils
