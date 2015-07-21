from __future__ import absolute_import

__all__ = ('withdraw',)

import logging
from logging import StreamHandler
from logging.handlers import SysLogHandler
import os
import requests
import sys

from bs4 import BeautifulSoup
from bs4.element import NavigableString

logger = logging.getLogger('bitcoin_testnet.haskoin_faucet')


class FaucetError(Exception):
    pass


class RateLimit(FaucetError):
    pass


class UnknownError(FaucetError):
    pass


def withdraw(address):
    """

    :param address: bitcoin address
    :return: tx hash
    :raise: FaucetError
    """

    logger.info('Withdrawing to {}'.format(address))

    response = requests.post(
        'http://faucet.haskoin.com/',
        {'address': address},
        stream=True)

    response.raise_for_status()

    html = response.text
    logger.debug(html)

    try:
        tx_hash = parse_tx_hash(html)
    except RateLimit:
        logger.warning('Rate limit exceeded.')
        raise

    if not tx_hash:
        m = "Couldn't find the tx hash."
        logger.error(m)
        raise UnknownError(m)

    logger.info('Tx hash {}'.format(tx_hash))
    return tx_hash


def parse_tx_hash(html):

    soup = BeautifulSoup(html)

    els = soup.select('.alert-success strong')

    if len(els) != 1:

        els = soup.select('.alert-danger')

        # "You are not authorized to withdraw yet"
        if any('withdraw yet' in el.text for el in els):
            raise RateLimit

        return

    children = list(els[0].children)

    if len(children) != 1:
        return

    node = children[0]

    if type(node) != NavigableString:
        return

    return str(node)


class SysLogFormatter(logging.Formatter):
    def format(self, record):
        return super(SysLogFormatter, self).format(record).replace('\n', ' | ')


def main():

    # Set the logger's handler
    log_target = os.environ.get('LOG_TARGET', 'stdout').lower().split(',')
    if 'syslog' in log_target:
        h = SysLogHandler(address='/dev/log')
        h.setFormatter(SysLogFormatter('haskoin_faucet: %(message)s'))
        logger.addHandler(h)
    if 'stdout' in log_target:
        logger.addHandler(StreamHandler())

    # Set the logger's level
    log_level = os.environ.get('LOG_LEVEL', 'info').upper()
    if log_level in ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']:
        logger.setLevel(getattr(logging, log_level))
    else:
        logger.warning('Unrecognized log level: {}'.format(log_level))

    # Verify there's exactly one argument
    if len(sys.argv) != 2:
        logger.error('Usage: haskoin_faucet <receiving_address>')
        return

    # Do the withdrawal
    try:
        withdraw(sys.argv[1])
    except FaucetError:
        sys.exit(1)
    except Exception:
        logger.exception('Uncaught exception.')
        sys.exit(2)

if __name__ == '__main__':
     main()
