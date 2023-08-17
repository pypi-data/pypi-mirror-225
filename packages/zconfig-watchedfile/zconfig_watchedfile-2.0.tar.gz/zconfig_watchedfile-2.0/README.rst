===================
zconfig_watchedfile
===================

Provides a ZConfig statement to register a logging handler that uses a
`WatchedFileHandler`_, which is helpful for integrating with an external
logrotate service::

    %import zconfig_watchedfile
    <logger>
      name example

      <watchedfile>
        path /path/to/logfile.log
      </watchedfile>
    </logger>

The ``<watchedfile>`` supports both the default ZConfig settings for handlers
(formatter, dateformat, level) and the parameters of `WatchedFileHandler`_
(mode, encoding, delay).

This package is compatible with Python version 3.8 up to 3.11.

.. _`WatchedFileHandler`: https://docs.python.org/3.11/library/logging.handlers.html#watchedfilehandler
