.. _auth:

################################
Authentication and authorisation
################################

DQSEGDB servers can be operated in a number of authorisation modes
depending on the access controls required.

The supported modes are detailed below.

.. _noauth:

=======
No auth
=======

DQSEGDB servers can be operated without requiring any
authorisation credentials.

.. _scitokens:

=========
SciTokens
=========

DQSEGDB servers may be operated with support for
`SciTokens <https://scitokens.org>`__, an implementation of
JSON Web Tokens designed for distributed scientific computing.

When using the :doc:`query functions <api>`, the following keyword arguments
can be used with all functions to control the use of SciTokens:

``token``
    **Default**: `None`

    A bearer token (:external+scitokens:class:`~scitokens.scitokens.SciToken`)
    to use to authorise the request.

    Pass ``token=False`` to disable any use of SciTokens.

``token_audience``
    **Default**: ``<scheme://host>`` (the fully-qualified ``host`` URI)

    The expected value of the ``aud`` token claim, which should match
    the fully-qualified URL of the GWDataFind host.

``token_scope``
    **Default**: ``"dqsegdb.read"``

    The expected value of ``scope`` token claim.
    At the time of writing, only ``"dqsegdb.read"`` is supported.

.. seealso::

    For full details on token arguments and how they are parsed, see
    :external+igwn-auth-utils:py:class:`igwn_auth_utils.Session`.

.. admonition:: SciTokens for IGWN

    SciTokens are the primary authorisation credential supported by
    the International Gravitational-Wave Observatory Network (IGWN),
    replacing X.509.

    If you can use scitokens instead of X.509, please do so.

    For full details on SciTokens for IGWN, please see
    https://computing.docs.ligo.org/guide/auth/scitokens/.

.. _x509:

=====
X.509
=====

DQSEGDB servers may also be configured to accept X.509 certificates or
proxies as authorisation credentials.
This requires the X.509 credential _subject_ to be known to the server
ahead of time.

When using the :doc:`API <api>`, the following keyword arguments
can be used to control the use of X.509 credentials:

``cert``
    **Default**: the value returned by
    :external+igwn-auth-utils:py:func:`igwn_auth_utils.find_x509_credentials`
    (or `None`)

    The path to an X.509 credential file.

    Pass `cert=False` to disable any use of X.509 credentials.

.. warning::

    X.509 as an authorisation credential is being deprecated by IGWN
    in favour of :ref:`scitokens`.

    If you can use scitokens instead of X.509, please do so.

    For full details on X.509 for IGWN, please see
    https://computing.docs.ligo.org/guide/auth/x509/.
