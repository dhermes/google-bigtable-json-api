from protorpc import messages

import dependency_messages
import operations_messages


class Zone(messages.Message):

    class Status(messages.Enum):
        # The state of the zone is unknown or unspecified.
        UNKNOWN = 0
        # The zone is in a good state.
        OK = 1
        # The zone is down for planned maintenance.
        PLANNED_MAINTENANCE = 2
        # The zone is down for emergency or unplanned maintenance.
        EMERGENCY_MAINENANCE = 3

    # A permanent unique identifier for the zone.
    # Values are of the form projects/<project>/zones/[a-z][-a-z0-9]*
    name = messages.StringField(1)
    # The name of this zone as it appears in UIs.
    display_name = messages.StringField(2)
    # The current state of this zone.
    status = messages.EnumField(Status, 3)


class StorageType(messages.Enum):
    # The storage type used is unspecified.
    STORAGE_UNSPECIFIED = 0
    # Data will be stored in SSD, providing low and consistent latencies.
    STORAGE_SSD = 1
    # Data will be stored in HDD, providing high and less predictable
    # latencies.
    STORAGE_HDD = 2


class Cluster(messages.Message):
    # A permanent unique identifier for the cluster. For technical reasons, the
    # zone in which the cluster resides is included here.
    # Values are of the form
    # projects/<project>/zones/<zone>/clusters/[a-z][-a-z0-9]*
    name = messages.StringField(1)
    # If this cluster has been deleted, the time at which its backup will
    # be irrevocably destroyed. Omitted otherwise.
    # This cannot be set directly, only through DeleteCluster.
    delete_time = messages.MessageField(dependency_messages.Timestamp, 2)
    # The operation currently running on the cluster, if any.
    # This cannot be set directly, only through CreateCluster, UpdateCluster,
    # or UndeleteCluster. Calls to these methods will be rejected if
    # "current_operation" is already set.
    current_operation = messages.MessageField(operations_messages.Operation, 3)
    # The descriptive name for this cluster as it appears in UIs.
    # Must be unique per zone.
    display_name = messages.StringField(4)
    # The number of serve nodes allocated to this cluster.
    serve_nodes = messages.IntegerField(5, variant=messages.Variant.INT32)
    # The maximum HDD storage usage allowed in this cluster, in bytes.
    hdd_bytes = messages.IntegerField(6, variant=messages.Variant.INT64)
    # The maximum SSD storage usage allowed in this cluster, in bytes.
    ssd_bytes = messages.IntegerField(7, variant=messages.Variant.INT64)
    # What storage type to use for tables in this cluster. Only configurable at
    # cluster creation time. If unspecified, STORAGE_SSD will be used.
    default_storage_type = messages.EnumField(StorageType, 8)


class ListZonesRequest(messages.Message):
    # The unique name of the project for which a list of supported zones is
    # requested.
    # Values are of the form projects/<project>
    name = messages.StringField(1)


class ListZonesResponse(messages.Message):
    # The list of requested zones.
    zones = messages.MessageField(Zone, 1, repeated=True)


class GetClusterRequest(messages.Message):
    # The unique name of the requested cluster.
    # Values are of the form projects/<project>/zones/<zone>/clusters/<cluster>
    name = messages.StringField(1)


class ListClustersRequest(messages.Message):
    # The unique name of the project for which a list of clusters is requested.
    # Values are of the form projects/<project>
    name = messages.StringField(1)


class ListClustersResponse(messages.Message):
    # The list of requested Clusters.
    clusters = messages.MessageField(Cluster, 1, repeated=True)
    # The zones for which clusters could not be retrieved.
    failed_zones = messages.MessageField(Zone, 2, repeated=True)


class CreateClusterRequest(messages.Message):
    # The unique name of the zone in which to create the cluster.
    # Values are of the form projects/<project>/zones/<zone>
    name = messages.StringField(1)
    # The id to be used when referring to the new cluster within its zone,
    # e.g. just the "test-cluster" section of the full name
    # "projects/<project>/zones/<zone>/clusters/test-cluster".
    cluster_id = messages.StringField(2)
    # The cluster to create.
    # The "name", "delete_time", and "current_operation" fields must be left
    # blank.
    cluster = messages.MessageField(Cluster, 3)


class CreateClusterMetadata(messages.Message):
    # The request which prompted the creation of this operation.
    original_request = messages.MessageField(CreateClusterRequest, 1)
    # The time at which original_request was received.
    request_time = messages.MessageField(dependency_messages.Timestamp, 2)
    # The time at which this operation failed or was completed successfully.
    finish_time = messages.MessageField(dependency_messages.Timestamp, 3)


class UpdateClusterMetadata(messages.Message):
    # The request which prompted the creation of this operation.
    original_request = messages.MessageField(Cluster, 1)
    # The time at which original_request was received.
    request_time = messages.MessageField(dependency_messages.Timestamp, 2)
    # The time at which this operation was cancelled. If set, this operation is
    # in the process of undoing itself (which is guaranteed to succeed) and
    # cannot be cancelled again.
    cancel_time = messages.MessageField(dependency_messages.Timestamp, 3)
    # The time at which this operation failed or was completed successfully.
    finish_time = messages.MessageField(dependency_messages.Timestamp, 4)


class DeleteClusterRequest(messages.Message):
    # The unique name of the cluster to be deleted.
    # Values are of the form projects/<project>/zones/<zone>/clusters/<cluster>
    name = messages.StringField(1)


class UndeleteClusterRequest(messages.Message):
    # The unique name of the cluster to be un-deleted.
    # Values are of the form projects/<project>/zones/<zone>/clusters/<cluster>
    name = messages.StringField(1)


class UndeleteClusterMetadata(messages.Message):
    # The time at which the original request was received.
    request_time = messages.MessageField(dependency_messages.Timestamp, 1)
    # The time at which this operation failed or was completed successfully.
    finish_time = messages.MessageField(dependency_messages.Timestamp, 2)
