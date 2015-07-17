from protorpc import messages


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


class Cluster(messages.Message):
    # A permanent unique identifier for the cluster. For technical reasons, the
    # zone in which the cluster resides is included here.
    # Values are of the form
    # projects/<project>/zones/<zone>/clusters/[a-z][-a-z0-9]*
    name = messages.StringField(1)
    # If this cluster has been deleted, the time at which its backup will
    # be irrevocably destroyed. Omitted otherwise.
    # This cannot be set directly, only through DeleteCluster.
    # NEEDED: google.protobuf.Timestamp delete_time = 2;
    # The operation currently running on the cluster, if any.
    # This cannot be set directly, only through CreateCluster, UpdateCluster,
    # or UndeleteCluster. Calls to these methods will be rejected if
    # "current_operation" is already set.
    # NEEDED: google.longrunning.Operation current_operation = 3;
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


class StorageType(messages.Enum):
    # The storage type used is unspecified.
    STORAGE_UNSPECIFIED = 0
    # Data will be stored in SSD, providing low and consistent latencies.
    STORAGE_SSD = 1
    # Data will be stored in HDD, providing high and less predictable
    # latencies.
    STORAGE_HDD = 2


class ListZonesRequest(messages.Message):
    pass


class ListZonesResponse(messages.Message):
    pass


class GetClusterRequest(messages.Message):
    pass


class ListClustersRequest(messages.Message):
    pass


class ListClustersResponse(messages.Message):
    pass


class CreateClusterRequest(messages.Message):
    pass


class CreateClusterMetadata(messages.Message):
    pass


class UpdateClusterMetadata(messages.Message):
    pass


class DeleteClusterRequest(messages.Message):
    pass


class UndeleteClusterRequest(messages.Message):
    pass


class UndeleteClusterMetadata(messages.Message):
    pass
