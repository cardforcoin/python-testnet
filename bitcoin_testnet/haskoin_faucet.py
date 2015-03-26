from __future__ import absolute_import

__all__ = ('withdraw',)

from bs4 import BeautifulSoup
from bs4.element import NavigableString
import requests


class RateLimit(Exception):
    pass


def withdraw(address):

    response = requests.post(
        'http://faucet.haskoin.com/',
        {'address': address},
        stream=True)

    response.raise_for_status()

    html = response.content

    tx_hash = parse_tx_hash(html)

    if not tx_hash:
        raise Exception("Couldn't find the transaction id."
                        " Maybe it didn't work?\n\n" + html)

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


if __name__ == '__main__':
    import sys
    try:
        print('Tx hash: {}'.format(withdraw(sys.argv[1])))
    except RateLimit:
        print('Rate limit exceeded.')
