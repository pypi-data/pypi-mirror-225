import logging
import os
import sys

from izaber.startup import initializer, request_initialize
from izaber.zconfig import config

class Logger(object):
    _logger = None

    def __call__(self,*args,**kwargs):
        self.info(*args,**kwargs)

    def __getattr__(self,k):
        if not self._logger:
            self._logger = logging.getLogger('main')
        return getattr(self._logger,k)

log = Logger()

@initializer('logging')
def initialize(**kwargs):
    request_initialize('config',**kwargs)
    logging_config = config.get('logging',{})
    logging_config.update( kwargs.get('logging',{}) )

    # We only activate logging if the logging section has
    # configuration. This allows users to configure their
    # own logger as desired
    if not logging_config:
        return

    # We also allow the disabling of the internally made logging module
    # by adding the logging.disable_internal key
    if logging_config.get('disable_internal'):
        return

    # So we have some logging configuration, let's let izaber setup a logging
    # handler.

    # If there's no filename, let's default to stream output for logging
    if 'filename' not in logging_config:
        logging_config.setdefault('stream', sys.stdout)

    # so there's a filename but it's blank, let's default to something
    elif not logging_config['filename']:
        for log_location in ['/tmp','/temp','.']:
            if not os.path.isdir(log_location):
                continue
            logging_config.setdefault('filename',os.path.join(log_location,'log.log'))
            break
    logging_config.setdefault('filemode','a')
    logging_config.setdefault(
        'format',
        '%(levelname)s %(asctime)s %(module)s: %(message)s'
    )
    logging_config.setdefault('datefmt','%Y-%m-%d %H:%M:%S')
    logging_config.setdefault('level',logging.WARNING)

    logging.basicConfig(**logging_config)

