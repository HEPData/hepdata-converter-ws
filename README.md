[![GitHub Actions Status](https://github.com/HEPData/hepdata-converter-ws/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/HEPData/hepdata-converter-ws/actions?query=branch%3Amain)
[![Coveralls Status](https://coveralls.io/repos/github/HEPData/hepdata-converter-ws/badge.svg?branch=main)](https://coveralls.io/github/HEPData/hepdata-converter-ws?branch=main)
[![License](https://img.shields.io/github/license/HEPData/hepdata-converter-ws.svg)](https://github.com/HEPData/hepdata-converter-ws/blob/main/LICENSE.txt)
[![GitHub Releases](https://img.shields.io/github/release/hepdata/hepdata-converter-ws.svg?maxAge=2592000)](https://github.com/HEPData/hepdata-converter-ws/releases)
[![PyPI Version](https://img.shields.io/pypi/v/hepdata-converter-ws)](https://pypi.org/project/hepdata-converter-ws/)
[![GitHub Issues](https://img.shields.io/github/issues/hepdata/hepdata-converter-ws.svg?maxAge=2592000)](https://github.com/HEPData/hepdata-converter-ws/issues)


# hepdata-converter-ws

Simple Flask Web Services wrapper in Python 3 for
[hepdata-converter](https://github.com/HEPData/hepdata-converter).

It allows running the
[hepdata-converter](https://github.com/HEPData/hepdata-converter) as a
web service on top of the [Flask](https://palletsprojects.com/p/flask/)
micro web framework.

## API

This web service provides one method which accepts `GET` JSON requests.
The accepted format is as follows:

### Request

```
[GET] /convert  (application/json)
{
input: Base64 encoded tar.gz file containing hepdata-converter-ws-data entry (directory / file)
id: str used for caching purposes (same input files have to have same ID), not implemented?
options: dictionary with options accepted by hepdata_converter.convert function. The most important are:
         input_format: (input format identifier e.g. yaml, oldhepdata, etc.)
         output_format: (output format identifier e.g. yaml, root, yoda, yoda1, csv, etc.)
         other options are dependent on the input / output format and are documented in their respective parsers / readers
         in https://github.com/HEPData/hepdata-converter
}
```

### Response

The response has MIME type `application/x-gzip` and is a tar.gz file
containing the hepdata-converter-ws-data directory with the
requested file/files.


## API Usage

It is recommended to use the
[hepdata-converter-ws-client](https://github.com/HEPData/hepdata-converter-ws-client)
library to interact with this web service, as it provides easier calling
and more transparent usage.