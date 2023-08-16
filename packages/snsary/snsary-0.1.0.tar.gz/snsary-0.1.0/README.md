# Snsary

A framework for sensor metrics.

## Installation

```bash
pip3 install snsary
```

## Getting started

Create a new file called example.py and paste:

```python
from snsary import system
from snsary.outputs import MockOutput
from snsary.sources import MockSensor
from snsary.utils import logging

MockSensor().subscribe(MockOutput())
logging.configure_logging()
system.start_and_wait()
```

This is a minimal Snsary program. To run it:

```bash
python3 example.py
```

At this point you should see some INFO logs e.g.

```bash
2021-11-13 19:07:17,144 - INFO - [mocksensor-4382645216] Collected 1 readings.
2021-11-13 19:07:17,144 - INFO - [mockoutput-4383959840] Reading: <zero 1636830437 0>
```

Use Ctrl+C to quit the program.

## Building an app

Snsary makes it easy to build large sensing apps:

- [In-built processing tools (API docs)](https://snsary.readthedocs.io/en/latest/).
- [Extra pre-built Sensors and Outputs](docs/extras/README.md).

[docs/examples/contrib.py](docs/examples/contrib.py) shows many of them working together.

## How to deploy it

[See the tutorial for how to setup and run a Snsary app as a service on a Raspberry Pi](docs/tutorial/README.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

See [LICENCE](LICENCE).
