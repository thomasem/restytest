# RestyTest

## Deployment

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

## Definitions/Assumptions

* Given the ambiguity in the industry for types of tests, I will be using the
  following definitions to describe each type of test:
    ** Unit: Unit tests are limited to the function boundary, so unit tests will
       exercise a particular function under manipulated inputs and outputs from
       dependent functions outside of the logic local to the function itself.
    ** Functional: Functional tests will be limited to the network boundary;
       anything using an external service will need to have that service mocked
       and returning mocked data that the can be manipulated in the test's
       context.
    ** Integration: Integration tests will err on the side of the highest
       possible fidelity; avoiding the use of mocks where viable, to assert real
       behavior of the integration between services.
* Given the scope of the exercise, I will be favoring integration tests as they
  have the highest return in terms of fidelity versus time spent.
* Durable data means in-memory and not persisted between restarts of the service
* The deployer will have the latest version of Python 2.7.x (2.7.12 as of this
  documentation.)

## Rationale

* I chose to use SQLAlchemy core only and avoid the ORM as I've typically found
  that the ORM tends to abstract the data architecture too far away, which seems
  prone to facilitating bad data architecture.
* SQLite is the default in-memory driver for SQLAlchemy and is sufficient for
  durable data.
