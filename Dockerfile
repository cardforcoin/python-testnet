FROM phusion/baseimage:0.9.16

RUN apt-get update && apt-get install -y python2.7 python-pip
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /opt/testnet
ADD bitcoin_testnet /opt/testnet/bitcoin_testnet
ADD setup.py /opt/testnet/
ADD *requirements.txt /opt/testnet/
RUN cd /opt/testnet && python setup.py install
