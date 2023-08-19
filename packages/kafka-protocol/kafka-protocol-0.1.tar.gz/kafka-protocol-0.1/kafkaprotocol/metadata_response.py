from .ktypes import *


class MetadataResponse0(Structure):
    FLEXIBLE = False
    brokers = ARRAY(
        node_id=INT32,
        host=STRING,
        port=INT32,
    )
    topics = ARRAY(
        error_code=INT16,
        name=STRING,
        partitions=ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            replica_nodes=ARRAY(INT32),
            isr_nodes=ARRAY(INT32),
        ),
    )


class MetadataResponse1(Structure):
    FLEXIBLE = False
    brokers = ARRAY(
        node_id=INT32,
        host=STRING,
        port=INT32,
        rack=NULLABLE_STRING,
    )
    controller_id = INT32
    topics = ARRAY(
        error_code=INT16,
        name=STRING,
        is_internal=BOOL,
        partitions=ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            replica_nodes=ARRAY(INT32),
            isr_nodes=ARRAY(INT32),
        ),
    )


class MetadataResponse2(Structure):
    FLEXIBLE = False
    brokers = ARRAY(
        node_id=INT32,
        host=STRING,
        port=INT32,
        rack=NULLABLE_STRING,
    )
    cluster_id = NULLABLE_STRING
    controller_id = INT32
    topics = ARRAY(
        error_code=INT16,
        name=STRING,
        is_internal=BOOL,
        partitions=ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            replica_nodes=ARRAY(INT32),
            isr_nodes=ARRAY(INT32),
        ),
    )


class MetadataResponse3(Structure):
    FLEXIBLE = False
    throttle_time_ms = INT32
    brokers = ARRAY(
        node_id=INT32,
        host=STRING,
        port=INT32,
        rack=NULLABLE_STRING,
    )
    cluster_id = NULLABLE_STRING
    controller_id = INT32
    topics = ARRAY(
        error_code=INT16,
        name=STRING,
        is_internal=BOOL,
        partitions=ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            replica_nodes=ARRAY(INT32),
            isr_nodes=ARRAY(INT32),
        ),
    )


class MetadataResponse4(Structure):
    FLEXIBLE = False
    throttle_time_ms = INT32
    brokers = ARRAY(
        node_id=INT32,
        host=STRING,
        port=INT32,
        rack=NULLABLE_STRING,
    )
    cluster_id = NULLABLE_STRING
    controller_id = INT32
    topics = ARRAY(
        error_code=INT16,
        name=STRING,
        is_internal=BOOL,
        partitions=ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            replica_nodes=ARRAY(INT32),
            isr_nodes=ARRAY(INT32),
        ),
    )


class MetadataResponse5(Structure):
    FLEXIBLE = False
    throttle_time_ms = INT32
    brokers = ARRAY(
        node_id=INT32,
        host=STRING,
        port=INT32,
        rack=NULLABLE_STRING,
    )
    cluster_id = NULLABLE_STRING
    controller_id = INT32
    topics = ARRAY(
        error_code=INT16,
        name=STRING,
        is_internal=BOOL,
        partitions=ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            replica_nodes=ARRAY(INT32),
            isr_nodes=ARRAY(INT32),
            offline_replicas=ARRAY(INT32),
        ),
    )


class MetadataResponse6(Structure):
    FLEXIBLE = False
    throttle_time_ms = INT32
    brokers = ARRAY(
        node_id=INT32,
        host=STRING,
        port=INT32,
        rack=NULLABLE_STRING,
    )
    cluster_id = NULLABLE_STRING
    controller_id = INT32
    topics = ARRAY(
        error_code=INT16,
        name=STRING,
        is_internal=BOOL,
        partitions=ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            replica_nodes=ARRAY(INT32),
            isr_nodes=ARRAY(INT32),
            offline_replicas=ARRAY(INT32),
        ),
    )


class MetadataResponse7(Structure):
    FLEXIBLE = False
    throttle_time_ms = INT32
    brokers = ARRAY(
        node_id=INT32,
        host=STRING,
        port=INT32,
        rack=NULLABLE_STRING,
    )
    cluster_id = NULLABLE_STRING
    controller_id = INT32
    topics = ARRAY(
        error_code=INT16,
        name=STRING,
        is_internal=BOOL,
        partitions=ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            leader_epoch=INT32,
            replica_nodes=ARRAY(INT32),
            isr_nodes=ARRAY(INT32),
            offline_replicas=ARRAY(INT32),
        ),
    )


class MetadataResponse8(Structure):
    FLEXIBLE = False
    throttle_time_ms = INT32
    brokers = ARRAY(
        node_id=INT32,
        host=STRING,
        port=INT32,
        rack=NULLABLE_STRING,
    )
    cluster_id = NULLABLE_STRING
    controller_id = INT32
    topics = ARRAY(
        error_code=INT16,
        name=STRING,
        is_internal=BOOL,
        partitions=ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            leader_epoch=INT32,
            replica_nodes=ARRAY(INT32),
            isr_nodes=ARRAY(INT32),
            offline_replicas=ARRAY(INT32),
        ),
        topic_authorized_operations=INT32,
    )
    cluster_authorized_operations = INT32


class MetadataResponse9(Structure):
    FLEXIBLE = True
    throttle_time_ms = INT32
    brokers = COMPACT_ARRAY(
        node_id=INT32,
        host=COMPACT_STRING,
        port=INT32,
        rack=COMPACT_NULLABLE_STRING,
        _tagged_fields=TAG_BUFFER,
    )
    cluster_id = COMPACT_NULLABLE_STRING
    controller_id = INT32
    topics = COMPACT_ARRAY(
        error_code=INT16,
        name=COMPACT_STRING,
        is_internal=BOOL,
        partitions=COMPACT_ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            leader_epoch=INT32,
            replica_nodes=COMPACT_ARRAY(INT32),
            isr_nodes=COMPACT_ARRAY(INT32),
            offline_replicas=COMPACT_ARRAY(INT32),
            _tagged_fields=TAG_BUFFER,
        ),
        topic_authorized_operations=INT32,
        _tagged_fields=TAG_BUFFER,
    )
    cluster_authorized_operations = INT32
    _tagged_fields = TAG_BUFFER


class MetadataResponse10(Structure):
    FLEXIBLE = True
    throttle_time_ms = INT32
    brokers = COMPACT_ARRAY(
        node_id=INT32,
        host=COMPACT_STRING,
        port=INT32,
        rack=COMPACT_NULLABLE_STRING,
        _tagged_fields=TAG_BUFFER,
    )
    cluster_id = COMPACT_NULLABLE_STRING
    controller_id = INT32
    topics = COMPACT_ARRAY(
        error_code=INT16,
        name=COMPACT_STRING,
        topic_id=UUID,
        is_internal=BOOL,
        partitions=COMPACT_ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            leader_epoch=INT32,
            replica_nodes=COMPACT_ARRAY(INT32),
            isr_nodes=COMPACT_ARRAY(INT32),
            offline_replicas=COMPACT_ARRAY(INT32),
            _tagged_fields=TAG_BUFFER,
        ),
        topic_authorized_operations=INT32,
        _tagged_fields=TAG_BUFFER,
    )
    cluster_authorized_operations = INT32
    _tagged_fields = TAG_BUFFER


class MetadataResponse11(Structure):
    FLEXIBLE = True
    throttle_time_ms = INT32
    brokers = COMPACT_ARRAY(
        node_id=INT32,
        host=COMPACT_STRING,
        port=INT32,
        rack=COMPACT_NULLABLE_STRING,
        _tagged_fields=TAG_BUFFER,
    )
    cluster_id = COMPACT_NULLABLE_STRING
    controller_id = INT32
    topics = COMPACT_ARRAY(
        error_code=INT16,
        name=COMPACT_STRING,
        topic_id=UUID,
        is_internal=BOOL,
        partitions=COMPACT_ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            leader_epoch=INT32,
            replica_nodes=COMPACT_ARRAY(INT32),
            isr_nodes=COMPACT_ARRAY(INT32),
            offline_replicas=COMPACT_ARRAY(INT32),
            _tagged_fields=TAG_BUFFER,
        ),
        topic_authorized_operations=INT32,
        _tagged_fields=TAG_BUFFER,
    )
    _tagged_fields = TAG_BUFFER


class MetadataResponse12(Structure):
    FLEXIBLE = True
    throttle_time_ms = INT32
    brokers = COMPACT_ARRAY(
        node_id=INT32,
        host=COMPACT_STRING,
        port=INT32,
        rack=COMPACT_NULLABLE_STRING,
        _tagged_fields=TAG_BUFFER,
    )
    cluster_id = COMPACT_NULLABLE_STRING
    controller_id = INT32
    topics = COMPACT_ARRAY(
        error_code=INT16,
        name=COMPACT_STRING,
        topic_id=UUID,
        is_internal=BOOL,
        partitions=COMPACT_ARRAY(
            error_code=INT16,
            partition_index=INT32,
            leader_id=INT32,
            leader_epoch=INT32,
            replica_nodes=COMPACT_ARRAY(INT32),
            isr_nodes=COMPACT_ARRAY(INT32),
            offline_replicas=COMPACT_ARRAY(INT32),
            _tagged_fields=TAG_BUFFER,
        ),
        topic_authorized_operations=INT32,
        _tagged_fields=TAG_BUFFER,
    )
    _tagged_fields = TAG_BUFFER


MetadataResponse = [
    MetadataResponse0,
    MetadataResponse1,
    MetadataResponse2,
    MetadataResponse3,
    MetadataResponse4,
    MetadataResponse5,
    MetadataResponse6,
    MetadataResponse7,
    MetadataResponse8,
    MetadataResponse9,
    MetadataResponse10,
    MetadataResponse11,
    MetadataResponse12,
]
