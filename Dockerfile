FROM python:3.4.3-onbuild

RUN cd /usr/src/app && python setup.py install
