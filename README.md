# AllDebrid Python API

This project provides a Python API for AllDebrid.

## Installation

To install, simply clone the repository and install the required packages listed in `requirements.txt` using pip:

    $ git clone https://github.com/unicorns18/alldebrid.py
    $ cd alldebrid
    $ pip install -r requirements.txt

## Usage
```python
from alldebrid import AllDebrid

# Create an instance of the AllDebrid class
ad = AllDebrid(api_key='YOUR_API_KEY')

ping = alldebrid.ping()
print('Ping:', ping)
```

## Tests

To run the tests:

    $ cd tests/
    $ pytest

## Acknowledgments

* [AllDebrid API Documentation](https://docs.alldebrid.com/) for providing the API documentation
