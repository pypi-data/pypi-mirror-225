import logging


class NullHandler(logging.Handler):
    """handler to avoid logging errors for, e.g., missing logger setup"""
    def emit(self, record):
        pass


logger = logging.getLogger(__name__)
logger.addHandler(NullHandler())
