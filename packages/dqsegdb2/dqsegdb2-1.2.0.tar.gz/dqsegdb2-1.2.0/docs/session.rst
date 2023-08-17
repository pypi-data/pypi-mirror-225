.. _dqsegdb2-session:

#############
Session usage
#############

All of the functions introduced in the :ref:`dqsegdb2-top-api` accept
a ``session`` keyword to enable reusing a connection to a DQSEGDB
host.

For example:

.. code-block:: python
    :caption: Example use of a :external+igwn-auth-utils:py:class:`igwn_auth_utils.Session` to reuse a connection.
    :name: dqsegdb2-session-example

    >>> from dqsegdb2 import (
    ...     query_segments,
    ...     Session,
    ... )
    >>> with Session() as sess:
    ...     segments = {}
    ...     for ifo, flag in (
    ...         ("G1", "G1:SCIENCE:1"),
    ...         ("H1", "H1:SCIENCE:1"),
    ...         ("L1", "L1:SCIENCE:1"),
    ...         ("V1", "V1:SCIENCE:1"),
    ...     ):
    ...         segments[ifo] = query_segments(
    ...             flag,
    ...             1187008880,
    ...             1187008884,
    ...             host="https://segments.igwn.org",
    ...             session=sess,
    ...         )

(The flag names in the above example are not real flag names.)

In the above example the connection to ``https://segments.igwn.org`` is
held open and reused to simplify subsequent queries and minimise the risk
of network communication issues.

The `dqsegdb2.Session` object is just an import of
:external+igwn-auth-utils:py:class:`igwn_auth_utils.Session`,
a wrapper around :external+requests:py:class:`requests.Session` that
automatically handles IGWN authorisation credentials/tokens.
For more details on credential or token usage, see :doc:`auth`.
