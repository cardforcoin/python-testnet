from __future__ import absolute_import

import sure  # pylint: disable=unused-import

import os

from bitcoin_testnet.haskoin_faucet import parse_tx_hash, RateLimit

TX_HASH = '9b95f245c918b7029b9debe06a41f538894cbb1d351cd792d3e6cf7fa3854d85'


def get_path(name):
    return os.path.join(os.path.dirname(__file__), name)


def test_parse_success():
    parse_tx_hash(open(get_path('success.html'))) \
        .should.equal(TX_HASH)


def test_parse_rate_limit():
    (lambda: parse_tx_hash(open(get_path('rate-limit.html')))) \
        .should.throw(RateLimit)
