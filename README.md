# hepdata-converter-ws

[![Join the chat at https://gitter.im/HEPData/hepdata-converter-ws](https://badges.gitter.im/HEPData/hepdata-converter-ws.svg)](https://gitter.im/HEPData/hepdata-converter-ws?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Simple Flask Web Services wrapper for hepdata-converter (https://github.com/HEPData/hepdata-converter)

It allows running hepdata-converter as a web service on top of flask micro framework.

## API

This web service provides one method which accepts GET JSON requests. Accepted format is as follows:

### Request

```
[GET] /convert  (application/json)
{
input: *base64 encoded tar.gz containing hepdata-converter-ws-data entry (directory / file)*
id: str used for caching purposes (same input files have to have same ID)
options: dictionary with options accepted by hepdata_converter.convert function. The most important are:
         input_format: (input format identifier eg. yaml, yoda, oldhepdata, etc)
         ouptut_format: (output format identifier eg. yaml, yoda, csv, etc)
         other options are dependant on the input / output format and are documented in their respected parsers / readers
         in (https://github.com/HEPData/hepdata-converter/)
}
```

### Response

Response has MIME type ```application/x-gzip``` and is a tar.gz file containing hepdata-converter-ws-data directory
with requested file / files


## API Usage

It is recommended to use hepdata-converter-ws-client library to interact with this web service
(https://github.com/HEPData/hepdata-converter-ws-client/) it provides easier calling and more transparent
usage.