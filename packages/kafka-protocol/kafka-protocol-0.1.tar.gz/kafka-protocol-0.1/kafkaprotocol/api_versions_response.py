from .ktypes import *


class ApiVersionsResponse0(Structure):
    FLEXIBLE = False
    error_code = INT16
    api_keys = ARRAY(
        api_key=INT16,
        min_version=INT16,
        max_version=INT16,
    )


class ApiVersionsResponse1(Structure):
    FLEXIBLE = False
    error_code = INT16
    api_keys = ARRAY(
        api_key=INT16,
        min_version=INT16,
        max_version=INT16,
    )
    throttle_time_ms = INT32


class ApiVersionsResponse2(Structure):
    FLEXIBLE = False
    error_code = INT16
    api_keys = ARRAY(
        api_key=INT16,
        min_version=INT16,
        max_version=INT16,
    )
    throttle_time_ms = INT32


class ApiVersionsResponse3(Structure):
    FLEXIBLE = True
    error_code = INT16
    api_keys = COMPACT_ARRAY(
        api_key=INT16, min_version=INT16, max_version=INT16, _tagged_fields=TAG_BUFFER
    )
    throttle_time_ms = INT32
    _tagged_fields = TAG_BUFFER


ApiVersionsResponse = [
    ApiVersionsResponse0,
    ApiVersionsResponse1,
    ApiVersionsResponse2,
    ApiVersionsResponse3,
]
