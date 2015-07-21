Python utils for using the bitcoin testnet.

# Haskoin faucet

Currently, the only thing in this repo is a procedure to pull test coins from
[faucet.haskoin.com](http://faucet.haskoin.com/).

### Shell

```
$ python -m bitcoin_testnet.haskoin_faucet 2MwXndSNLYbD9smwjmuMDFdQMW3ccGN9dLx
Tx hash: 151cca1ea8d82208da1a2b7508adbd8395b75f07e2d684d4bd245488d28d4950
```

### Environment variables

* `LOG_TARGET` — Comma-separated list of logging destinations.
  Options are `syslog` and `stdout`. Default: `stdout`.

* `LOG_LEVEL` — One of the following:
  `critical`, `error`, `warning`, `info`, `debug`.
  Default: `info`.

### Docker

```
$ docker build -t testnet .
...

$ docker run testnet python -m bitcoin_testnet.haskoin_faucet 2MwXndSNLYbD9smwjmuMDFdQMW3ccGN9dLx
Tx hash: a14577329eb4e36fdb1308329fee73d546dcddca8eda2e7498a2b413c674539f
```
