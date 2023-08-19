from .ktypes import (
    BytesIO,
    RequestHeader0,
    RequestHeader1,
    RequestHeader2,
    ResponseHeader0,
    ResponseHeader1,
    TAG_BUFFER,
)
from .api_versions_request import ApiVersionsRequest
from .api_versions_response import ApiVersionsResponse
from .metadata_request import MetadataRequest
from .metadata_response import MetadataResponse


requests = {
    3: MetadataRequest,
    18: ApiVersionsRequest,
}
responses = {
    3: MetadataResponse,
    18: ApiVersionsResponse,
}


def read_network_request(data: bytes):
    bytesio = BytesIO(data[4:])
    # header = RequestHeader2.unpack(bytesio)
    header = RequestHeader1.unpack(bytesio)
    messageklass = requests[header.request_api_key][header.request_api_version]

    if messageklass.FLEXIBLE:
        _ = TAG_BUFFER.unpack(bytesio)

    message = messageklass.unpack(bytesio)

    assert bytesio.read() == b""
    return (header, message)


def read_network_response(key, version, data: bytes):
    bytesio = BytesIO(data[4:])
    # header = ResponseHeader1.unpack(bytesio)
    header = ResponseHeader0.unpack(bytesio)
    messageklass = responses[key][version]

    if key == 18:
        # Version 3 is the first flexible version. Tagged fields are only supported in the body but
        # not in the header. The length of the header must not change in order to guarantee the
        # backward compatibility.
        pass
    elif messageklass.FLEXIBLE:
        _ = TAG_BUFFER.unpack(bytesio)

    message = messageklass.unpack(bytesio)

    assert bytesio.read() == b""
    return (header, message)
