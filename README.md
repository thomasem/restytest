# RestyTest

## Deployment (w/o Docker)

### Environment assumptions
* Linux or OS X
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

### Run

```bash
$ restytest
...
```

## Deployment (w/ Docker)

### Environment assumptions

* `HOST_PORT` is an environment variable set to the port you wish to expose on
  the host you're deploying this service to. Otherwise you can use `-P` in place
  of `-p $HOST_PORT:8080` and then `docker port restytest 8080/tcp` to get the
  location address and port the server is listening on.

### Hosted image

```bash
$ docker run -d --name restytest -p $HOST_PORT:8080 tmaddox/restytest
...
```

### Local build

```bash
$ docker build -t restytest .
...
$ docker run -d --name restytest -p $HOST_PORT:8080 restytest
...
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

* The returned objects from the `/groups` endpoint were inconsistent and
  would be confusing for an end-user to work with at first.
