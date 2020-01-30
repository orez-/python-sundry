import collections
import contextlib
import logging


class QueryHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.queries = []
        self.addFilter(lambda record: record.msg.startswith('SELECT '))

    def emit(self, record):
        print(record)
        self.queries.append(record.getMessage())

    def top_queries(self):
        return collections.Counter(self.queries).most_common()


@contextlib.contextmanager
def logging_context(handler):
    logger = logging.getLogger()

    logger.addHandler(handler)
    yield handler
    logger.removeHandler(handler)


#  ---

import pytest


def test_log():
    logger = logging.getLogger("doesn't matter")
    logger.setLevel(logging.INFO)
    handler = QueryHandler()

    logger.info("one")
    logger.info("SELECT one")
    with logging_context(handler):
        logger.info("two")
        logger.info("SELECT two")
        logger.info("three")
        logger.info("SELECT three")
    logger.info("four")
    logger.info("SELECT four")

    assert handler.queries == ['SELECT two', 'SELECT three']


def test_reusable():
    logger = logging.getLogger('anything')
    logger.setLevel(logging.INFO)

    handle_fizz = QueryHandler()
    handle_buzz = QueryHandler()

    for i in range(1, 8):
        with logging_context(handle_fizz):
            if i % 3:
                logger.info("SELECT %s", i)
            else:
                logger.info("SELECT fizz")

        with logging_context(handle_buzz):
            if i % 5:
                logger.info("SELECT %s", i)
            else:
                logger.info("SELECT buzz")

    assert handle_fizz.queries == ['SELECT 1', 'SELECT 2', 'SELECT fizz', 'SELECT 4', 'SELECT 5', 'SELECT fizz', 'SELECT 7']
    assert handle_buzz.queries == ['SELECT 1', 'SELECT 2', 'SELECT 3', 'SELECT 4', 'SELECT buzz', 'SELECT 6', 'SELECT 7']
