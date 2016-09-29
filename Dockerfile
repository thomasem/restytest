FROM python:2.7

MAINTAINER Thomas Maddox <thomas.e.maddox@gmail.com>

WORKDIR /restytest

COPY . .

RUN python setup.py install

ENV RESTYTEST_HOST=0.0.0.0
ENV RESTYTEST_PORT=8080

EXPOSE $RESTYTEST_PORT

ENTRYPOINT ["restytest"]