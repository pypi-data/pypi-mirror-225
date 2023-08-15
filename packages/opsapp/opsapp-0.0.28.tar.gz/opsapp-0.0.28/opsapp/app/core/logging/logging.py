# encoding: utf-8
"""
@author: linvaux
@contact: linvaux@outlook.com
@time: 2020/2/22 22:03
@desc: 日志
"""

import datetime
import logging
import os
from logging import handlers

from ...settings.config import LOG_DIR

try:
    log_level = os.environ['LOG_LEVEL']
except KeyError:
    log_level = 'info'  # pylint: disable=invalid-name (C0103)


class LoggerFactory:
    """
    Manage log
    """
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARNING,
        'error': logging.ERROR,
    }

    def __init__(self, filename='log', when='D', back_count=3,
                 fmt='%(asctime)s | %(levelname)s| %(module)s:%(funcName)s:%(lineno)d - %(message)s'):
        """
        保存日志
        Args:
            filename: log file name
            when: saved by day
            back_count:
            fmt: log format
        """
        if not os.path.exists(LOG_DIR):
            os.mkdir(LOG_DIR)
            #  这里进行判断，如果logger.handlers列表为空，则添加，否则，直接去写日志
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(LOG_DIR, filename + "-" + today + ".log")
        self.logger = logging.getLogger(filename) 
        if not self.logger.handlers:   
            logging.addLevelName(logging.CRITICAL, logging.getLevelName(logging.CRITICAL).ljust(9))
            logging.addLevelName(logging.FATAL, logging.getLevelName(logging.FATAL).ljust(9))
            logging.addLevelName(logging.ERROR, logging.getLevelName(logging.ERROR).ljust(9))
            logging.addLevelName(logging.WARNING, logging.getLevelName(logging.WARNING).ljust(9))
            logging.addLevelName(logging.INFO, logging.getLevelName(logging.INFO).ljust(9))
            logging.addLevelName(logging.DEBUG, logging.getLevelName(logging.DEBUG).ljust(9))
            logging.addLevelName(logging.NOTSET, logging.getLevelName(logging.NOTSET).ljust(9))
            
            format_str = logging.Formatter(fmt)
            self.logger.setLevel(self.level_relations[log_level]) 
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(format_str)
            file_handler = handlers.TimedRotatingFileHandler(filename=log_file, when=when, backupCount=back_count,
                                                             encoding='utf-8')
            file_handler.setFormatter(format_str)
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
         
