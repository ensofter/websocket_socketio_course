import logging
import os
from datetime import datetime


class MyLogger:
    _logger = None

    def __new__(cls, *args, **kwargs):
        if cls._logger is None:
            print('Logger new')
            cls._logger = logging.getLogger(__name__)
            cls._logger.setLevel('DEBUG')
            formatter = logging.Formatter(
                '%(asctime)s - [%(levelname)s | %(filename)s:%(lineno)s > %(message)s'
            )
            now = datetime.now()
            dirname = './log'

            if not os.path.isdir(dirname):
                os.mkdir(dirname)
            fileHandler = logging.FileHandler(
                dirname + '/log_' + now.strftime('%Y-%m-%d'+'.log')
            )

            sreamHandler = logging.StreamHandler()

            fileHandler.setFormatter(formatter)
            sreamHandler.setFormatter(formatter)

            cls._logger.addHandler(fileHandler)
            cls._logger.addHandler(sreamHandler)
        return cls._logger
