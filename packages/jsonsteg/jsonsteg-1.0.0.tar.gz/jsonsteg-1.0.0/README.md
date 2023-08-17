# JSON steganography

_Write payload into JSON without modifying it_	

![Python version](https://img.shields.io/pypi/pyversions/jsonsteg)
![Build status](https://github.com/PyryL/jsonsteg/actions/workflows/main.yml/badge.svg)
![Branch coverage](https://codecov.io/gh/PyryL/jsonsteg/branch/main/graph/badge.svg?token=YT08CLBMMK)
[![PyPI](https://img.shields.io/pypi/v/jsonsteg)](https://pypi.org/project/jsonsteg/)


## Installation

Install jsonsteg via [PyPI](https://pypi.org/project/jsonsteg/):

```
pip install jsonsteg
```


## CLI usage

Use command line interface via `jsonsteg` command.

### Writing

Write payload `mysecret` to JSON found in file `data.json`:

```
jsonsteg write --input mysecret data.json
```

Write the contents of file `message.txt` as a payload to JSON of file `data.json`:

```
jsonsteg write --input-file message.txt data.json
```

Instead of modifying `data.json` file, you can output the altered JSON to `output.json` file:

```
jsonsteg write --input mysecret --output output.json data.json
```

### Reading

Write the payload of JSON in file `data.json` and print it to console:

```
jsonsteg read data.json
```

Instead of printing, the output can also be saved to file `output.txt`:

```
jsonsteg read --output output.txt data.json
```

### Help

Learn more about possible options with these commands:

```
jsonsteg --help
jsonsteg read --help
jsonsteg write --help
```


## Python usage

Jsonsteg can also be used as a Python package:

```
import jsonsteg

jsonsteg.DictionaryReader(json_dictionary)
jsonsteg.DictionaryWriter(json_dictionary, payload_bytes)
jsonsteg.ArrayReader(json_array)
jsonsteg.ArrayWriter(json_array, payload_bytes)
```

Writer objects have `output` property and reader objects have `payload` property.


## Development

After cloning the git repository, install development dependencies
by running the following command in project root:

```
poetry install
```

Run unit tests with

```
poetry run invoke test
```

Run coverage test with

```
poetry run invoke coverage
```

and create HTML coverage report with

```
poetry run invoke coverage-report
```

Publish the package on pypi.org or test.pypi.org by one of the following commands:

```
poetry run invoke publish
poetry run invoke publish-test
```

When running either one of the commands above,
you must have PYPI token stored in an environment variable named
`POETRY_PYPI_TOKEN_PYPI` or `POETRY_PYPI_TOKEN_TEST_PYPI`, respectively.


## How is it done?

Read more about the mechanism [here](docs/mechanism.md).
