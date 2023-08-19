from .ktypes import *


class ApiVersionsRequest0(Structure):
    FLEXIBLE = False
    pass


class ApiVersionsRequest1(Structure):
    FLEXIBLE = False
    pass


class ApiVersionsRequest2(Structure):
    FLEXIBLE = False
    pass


class ApiVersionsRequest3(Structure):
    FLEXIBLE = True
    client_software_name = COMPACT_STRING
    client_software_version = COMPACT_STRING
    _tagged_fields = TAG_BUFFER


ApiVersionsRequest = [
    ApiVersionsRequest0,
    ApiVersionsRequest1,
    ApiVersionsRequest2,
    ApiVersionsRequest3,
]
