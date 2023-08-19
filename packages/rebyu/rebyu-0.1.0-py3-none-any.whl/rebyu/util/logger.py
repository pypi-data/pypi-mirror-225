import sys

from typing import AnyStr

from loguru import logger


class Logger(object):

    def __init__(self, class_name):
        self.class_name = class_name
        self.ctx_log = logger.bind(name=class_name)

    def info(self, message: AnyStr):
        self.ctx_log.info(message)

    def warning(self, message: AnyStr):
        self.ctx_log.warning(message)

    def error(self, message: AnyStr):
        self.ctx_log.error(message)
