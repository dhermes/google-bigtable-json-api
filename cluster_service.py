import endpoints

from protorpc import messages
from protorpc import remote

import cluster_messages
import dependency_messages
import operations_messages
from scopes import ADMIN_SCOPE


LIST_ZONES_CONTAINER = endpoints.ResourceContainer(
    cluster_messages.ListZonesRequest,
    name = messages.StringField(1, required=True),
)
GET_CLUSTER_CONTAINER = endpoints.ResourceContainer(
    cluster_messages.GetClusterRequest,
    name = messages.StringField(1, required=True),
)
LIST_CLUSTERS_CONTAINER = endpoints.ResourceContainer(
    cluster_messages.ListClustersRequest,
    name = messages.StringField(1, required=True),
)
CREATE_CLUSTER_CONTAINER = endpoints.ResourceContainer(
    cluster_messages.CreateClusterRequest,
    name = messages.StringField(1, required=True),
)

# Local version of Cluster with no name property, to avoid
# collision in the ResourceContainer.
class Cluster(messages.Message):
    delete_time = messages.MessageField(dependency_messages.Timestamp, 2)
    current_operation = messages.MessageField(operations_messages.Operation, 3)
    display_name = messages.StringField(4)
    serve_nodes = messages.IntegerField(5, variant=messages.Variant.INT32)
    hdd_bytes = messages.IntegerField(6, variant=messages.Variant.INT64)
    ssd_bytes = messages.IntegerField(7, variant=messages.Variant.INT64)
    default_storage_type = messages.EnumField(cluster_messages.StorageType, 8)


UPDATE_CLUSTER_CONTAINER = endpoints.ResourceContainer(
    Cluster,
    name = messages.StringField(1, required=True),
)
DELETE_CLUSTER_CONTAINER = endpoints.ResourceContainer(
    cluster_messages.DeleteClusterRequest,
    name = messages.StringField(1, required=True),
)
UNDELETE_CLUSTER_CONTAINER = endpoints.ResourceContainer(
    cluster_messages.UndeleteClusterRequest,
    name = messages.StringField(1, required=True),
)


@endpoints.api(name='bigtableclusteradmin', version='v1',
               description='Bigtable Cluster Admin API',
               hostname='bigtableclusteradmin.googleapis.com',
               scopes=(ADMIN_SCOPE,))
class BigtableClusterService(remote.Service):

    @endpoints.method(LIST_ZONES_CONTAINER, cluster_messages.ListZonesResponse,
                      http_method='GET', name='clusters.listzones',
                      path='{name}/zones')
    def ListZones(self, request):
        """Lists the supported zones for the given project."""
        return cluster_messages.ListZonesResponse()

    @endpoints.method(GET_CLUSTER_CONTAINER, cluster_messages.Cluster,
                      http_method='GET', name='clusters.get',
                      path='{name}')
    def GetCluster(self, request):
        """Gets information about a particular cluster."""
        return cluster_messages.Cluster()

    @endpoints.method(LIST_CLUSTERS_CONTAINER,
                      cluster_messages.ListClustersResponse,
                      http_method='GET', name='clusters.list',
                      path='{name}/aggregated/clusters')
    def ListClusters(self, request):
        """Lists clusters.

        Lists all clusters in the given project, along with any zones for which
        cluster information could not be retrieved.
        """
        return cluster_messages.ListClustersResponse()

    @endpoints.method(CREATE_CLUSTER_CONTAINER, cluster_messages.Cluster,
                      http_method='POST', name='clusters.create',
                      path='{name}/clusters')
    def CreateCluster(self, request):
        """Creates a cluster.

        Creates a cluster and begins preparing it to begin serving. The
        returned cluster embeds as its "current_operation" a long-running
        operation which can be used to track the progress of turning up the
        new cluster. Immediately upon completion of this request:
         * The cluster will be readable via the API, with all requested
           attributes but no allocated resources.
        Until completion of the embedded operation:
         * Cancelling the operation will render the cluster immediately
           unreadable via the API.
         * All other attempts to modify or delete the cluster will be rejected.
        Upon completion of the embedded operation:
         * Billing for all successfully-allocated resources will begin (some
           types may have lower than the requested levels).
         * New tables can be created in the cluster.
         * The cluster's allocated resource levels will be readable via the
           API.
        The embedded operation's "metadata" field type is
        [CreateClusterMetadata][google.bigtable.admin.cluster.v1.CreateClusterMetadata] The embedded operation's "response" field type is
        [Cluster][google.bigtable.admin.cluster.v1.Cluster], if successful.
        """
        return cluster_messages.Cluster()

    @endpoints.method(UPDATE_CLUSTER_CONTAINER, cluster_messages.Cluster,
                      http_method='PUT', name='clusters.update',
                      path='{name}')
    def UpdateCluster(self, request):
        """Updates cluster.

        Updates a cluster, and begins allocating or releasing resources as
        requested. The returned cluster embeds as its "current_operation" a
        long-running operation which can be used to track the progress of
        updating the cluster.
        Immediately upon completion of this request:
         * For resource types where a decrease in the cluster's allocation has
           been requested, billing will be based on the newly-requested level.
        Until completion of the embedded operation:
         * Cancelling the operation will set its metadata's
           "cancelled_at_time", and begin restoring resources to their
           pre-request values. The operation is guaranteed to succeed at
           undoing all resource changes, after which point it will terminate
           with a CANCELLED status.
         * All other attempts to modify or delete the cluster will be rejected.
         * Reading the cluster via the API will continue to give the
           pre-request resource levels.
        Upon completion of the embedded operation:
         * Billing will begin for all successfully-allocated resources (some
           types may have lower than the requested levels).
         * All newly-reserved resources will be available for serving the
           cluster's tables.
         * The cluster's new resource levels will be readable via the API.
        [UpdateClusterMetadata][google.bigtable.admin.cluster.v1.UpdateClusterMetadata] The embedded operation's "response" field type is
        [Cluster][google.bigtable.admin.cluster.v1.Cluster], if successful.
        """
        return cluster_messages.Cluster()

    @endpoints.method(DELETE_CLUSTER_CONTAINER, dependency_messages.Empty,
                      http_method='DELETE', name='clusters.delete',
                      path='{name}')
    def DeleteCluster(self, request):
        """Delete cluster.

        Marks a cluster and all of its tables for permanent deletion in 7 days.
        Immediately upon completion of the request:
         * Billing will cease for all of the cluster's reserved resources.
         * The cluster's "delete_time" field will be set 7 days in the future.
        Soon afterward:
         * All tables within the cluster will become unavailable.
        Prior to the cluster's "delete_time":
         * The cluster can be recovered with a call to UndeleteCluster.
         * All other attempts to modify or delete the cluster will be rejected.
        At the cluster's "delete_time":
         * The cluster and *all of its tables* will immediately and irrevocably
           disappear from the API, and their data will be permanently deleted.
        """
        return dependency_messages.Empty()

    # Path should actually be {name}:undelete but generator fails with
    # the colon, so we just replace it in the generated file.
    @endpoints.method(UNDELETE_CLUSTER_CONTAINER,
                      operations_messages.Operation,
                      http_method='POST', name='clusters.undelete',
                      path='{name}/undelete')
    def UndeleteCluster(self, request):
        """Undelete cluster.

        Cancels the scheduled deletion of an cluster and begins preparing it to
        resume serving. The returned operation will also be embedded as the
        cluster's "current_operation".
        Immediately upon completion of this request:
         * The cluster's "delete_time" field will be unset, protecting it from
           automatic deletion.
        Until completion of the returned operation:
         * The operation cannot be cancelled.
        Upon completion of the returned operation:
         * Billing for the cluster's resources will resume.
         * All tables within the cluster will be available.
        [UndeleteClusterMetadata][google.bigtable.admin.cluster.v1.UndeleteClusterMetadata] The embedded operation's "response" field type is
        [Cluster][google.bigtable.admin.cluster.v1.Cluster], if successful.
        """
        return operations_messages.Operation()
