# Result Reporter Client

This client will report results of a function execution to an endpoint. This
can be especially useful for determining how many students in a class are
successfully completing an exercise.


### Usage

```
import rr

# Define endpoint to send results to.
rr.set_global_endpoint('https://result-reporter.com/ingest')
# User-Assignment identification token. This is provided by Result-Reporter.com
rr.set_global_token('f0c3f-1234-abcd-1234-740e2cf8daf8')


def fibonacci(n: int) -> int:
    # Left for your students to implement.
    pass


# Tests provided for your students.
with rr.Wrap(fibonacci) as f:
    assert f(0) == 0
    assert f(1) == 1
    assert f(2) == 1
    assert f(3) == 2
    assert f(4) == 3
    assert f(5) == 5
    assert f(6) == 8
```

Results will then be available for visualization via the result server.

### Installation

```
$ pip install result-reporter
```
