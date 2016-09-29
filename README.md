# RestyTest

## Deployment (w/o Docker)

### Environment assumptions
* Linux OS (I suspect OS X will work as well, but don't have one to test)
* Python 2.7.12
* `tox` is installed for running tests

### Installation

```bash
$ python setup.py install
```

### Configuration

Configuration is done via the following environment variables:

* `RESTYTEST_HOST`: Address to listen for requests on (default: `localhost`)
* `RESTYTEST_PORT`: Port to listen to requests on (default: `8080`)

### Run with entrypoint script)

```bash
$ restytest
...
```

### Example

#### In one terminal

```bash
$ python setup.py install
running install
...
Finished processing dependencies for RestyTest==0.1.0
$ pyenv rehash
$ restytest
Bottle v0.12.9 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.
```

#### In another terminal

```bash
$ curl -X POST http://localhost:8080/groups -d '{"name": "admins"}' | jq .
{
  "userids": []
}
```

### Run without entrypoint script

```bash
$ pip install -r requirements.txt && pip install -e .
$ python restytest/api/app.py
Bottle v0.12.9 server starting up (using WSGIRefServer())...
Listening on http://localhost:8080/
Hit Ctrl-C to quit.
...
```

### Gotchas

* If you're using `pyenv` for setting up a virtualenv to install this package in
  be sure to run `pyenv rehash` after doing `python setup.py install`

## Deployment (w/ Docker)

### Environment assumptions

* `HOST_PORT` is an environment variable set to the port you wish to expose on
  the host you're deploying this service to. Otherwise you can use `-P` in place
  of `-p $HOST_PORT:8080` and then `docker port restytest 8080` to get the
  location address and port the server is listening on.

### Local build

```bash
$ docker build -t restytest .
...
$ docker run -d --name restytest -p $HOST_PORT:8080 restytest
...
```

### Example

```bash
$ docker build -t restytest .
Sending build context to Docker daemon 68.89 MB
Step 1 : FROM python:2.7
 ---> 6b494b5f019c
...
$ docker run -d --name restytest -P restytest
04e1dd26018c212dce62e70f23c143402093b014b1195b688a00f92dc47b2734
(planet) 21:23:33(-0500) ~/restytest {master} $ docker port restytest 8080
0.0.0.0:33039
(planet) 21:23:43(-0500) ~/restytest {master} $ curl -X POST http://localhost:33039/groups -d '{"name": "admins"}' | jq .
{
  "userids": []
}
```

## Running Tests

### Run the tests

```bash
$ pip install tox
...
$ tox
```
### Example

```bash
$ tox 
py27 installed: ...
py27 runtests: PYTHONHASHSEED='4263541967'
py27 runtests: commands[0] | nosetests --with-coverage --cover-erase --cover-package=restytest
..............................
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
restytest.py                       0      0   100%
restytest/api.py                   0      0   100%
restytest/api/app.py              61      0   100%
restytest/api/controller.py       59      0   100%
restytest/api/validations.py      27      0   100%
restytest/api/views.py             4      0   100%
restytest/exceptions.py           10      0   100%
restytest/models.py               10      0   100%
restytest/storage.py               2      0   100%
restytest/storage/impl.py         85      0   100%
restytest/storage/schema.py        5      0   100%
------------------------------------------------------------
TOTAL                            263      0   100%
----------------------------------------------------------------------
Ran 30 tests in 0.346s

OK
flake8 installed: ...
flake8 runtests: PYTHONHASHSEED='4263541967'
flake8 runtests: commands[0] | flake8
__________________________________________________________ summary ___________________________________________________________
  py27: commands succeeded
  flake8: commands succeeded
  congratulations :)
```

## Rationale

* I chose to use SQLAlchemy core only and avoid the ORM as I've typically found
  that the ORM tends to abstract the data architecture too far away, which seems
  prone to facilitating bad data architecture.

* SQLite is the default in-memory driver for SQLAlchemy and seems sufficient for
  durable data.

## Criticisms/Ponderings

* I feel like using `userid` as a string instead of a generated `id` or `uuid`
  identifier got in the way a fair bit. The possibility of a user
  submitting an entirely new User (via submitting a different `userid`) in place
  of their old one seemed a possibility for the noted specification which drove
  my design of the update functionality to entirely remove the "old" User and
  replace with the new valid User that was submitted. I think using generated
  identifiers and partial PUTs is usually a cleaner and easier design choice in
  the long run.

* Same goes for Groups. Seems like a numeric, generated ID would lend itself to
  cleaner design.

* Using in-memory (perhaps just SQLite) for durable storage left me without a
  clean way to collect, say, `groups` from a many-to-many relationship in one
  DB call. I wasn't wild about that fact. However, being in-memory means there's
  not a significant performance impact anyway.

* I wasn't sure what lengths were desired, so I went with the
  [UK Government Data Standards](http://webarchive.nationalarchives.gov.uk/20100407120701/http://cabinetoffice.gov.uk/govtalk/schemasstandards/e-gif/datastandards/person_information/person_name.aspx)
  specification of `35` characters.

* I also was unsure about the max number of groups we wanted to allow a user, so
  I chose `50` as a reasonable number for `RestyTest`.

* Using `{"name": "group_name"}` for creating a Group made for a bit of an
  awkward interface. Furthermore, it seems like one ought to be able to create
  a group and add a user to it in the same payload, and like the `POST /groups`
  ought to follow a similar pattern to `POST /users` in that you submit a valid
  Group object.

* The returned objects from the `/groups` endpoint were inconsistent with what
  was used to create the  and
  would be confusing for an end-user to work with at first.
