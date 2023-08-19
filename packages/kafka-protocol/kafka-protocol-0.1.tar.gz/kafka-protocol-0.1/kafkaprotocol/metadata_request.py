from .ktypes import *


class MetadataRequest0(Structure):
    FLEXIBLE = False
    topics = ARRAY(
        name=STRING,
    )


class MetadataRequest1(Structure):
    FLEXIBLE = False
    topics = ARRAY(
        name=STRING,
    )


class MetadataRequest2(Structure):
    FLEXIBLE = False
    topics = ARRAY(
        name=STRING,
    )


class MetadataRequest3(Structure):
    FLEXIBLE = False
    topics = ARRAY(
        name=STRING,
    )


class MetadataRequest4(Structure):
    FLEXIBLE = False
    topics = ARRAY(
        name=STRING,
    )
    allow_auto_topic_creation = BOOL


class MetadataRequest5(Structure):
    FLEXIBLE = False
    topics = ARRAY(
        name=STRING,
    )
    allow_auto_topic_creation = BOOL


class MetadataRequest6(Structure):
    FLEXIBLE = False
    topics = ARRAY(
        name=STRING,
    )
    allow_auto_topic_creation = BOOL


class MetadataRequest7(Structure):
    FLEXIBLE = False
    topics = ARRAY(
        name=STRING,
    )
    allow_auto_topic_creation = BOOL


class MetadataRequest8(Structure):
    FLEXIBLE = False
    topics = ARRAY(
        name=STRING,
    )
    allow_auto_topic_creation = BOOL
    include_cluster_authorized_operations = BOOL
    include_topic_authorized_operations = BOOL


class MetadataRequest9(Structure):
    FLEXIBLE = True
    topics = COMPACT_ARRAY(name=COMPACT_STRING, _tagged_fields=TAG_BUFFER)
    allow_auto_topic_creation = BOOL
    include_cluster_authorized_operations = BOOL
    include_topic_authorized_operations = BOOL
    _tagged_fields = TAG_BUFFER


class MetadataRequest10(Structure):
    FLEXIBLE = True
    topics = COMPACT_ARRAY(
        topic_id=UUID, name=COMPACT_STRING, _tagged_fields=TAG_BUFFER
    )
    allow_auto_topic_creation = BOOL
    include_cluster_authorized_operations = BOOL
    include_topic_authorized_operations = BOOL
    _tagged_fields = TAG_BUFFER


class MetadataRequest11(Structure):
    FLEXIBLE = True
    topics = COMPACT_ARRAY(
        topic_id=UUID, name=COMPACT_STRING, _tagged_fields=TAG_BUFFER
    )
    allow_auto_topic_creation = BOOL
    include_topic_authorized_operations = BOOL
    _tagged_fields = TAG_BUFFER


class MetadataRequest12(Structure):
    FLEXIBLE = True
    topics = COMPACT_ARRAY(
        topic_id=UUID, name=COMPACT_STRING, _tagged_fields=TAG_BUFFER
    )
    allow_auto_topic_creation = BOOL
    include_topic_authorized_operations = BOOL
    _tagged_fields = TAG_BUFFER


MetadataRequest = [
    MetadataRequest0,
    MetadataRequest1,
    MetadataRequest2,
    MetadataRequest3,
    MetadataRequest4,
    MetadataRequest5,
    MetadataRequest6,
    MetadataRequest7,
    MetadataRequest8,
    MetadataRequest9,
    MetadataRequest10,
    MetadataRequest11,
    MetadataRequest12,
]
