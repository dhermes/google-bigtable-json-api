from protorpc import remote

import cluster_messages
import dependency_messages


class BigtableClusterService(remote.Service):

    def ListZones(self, request):
        """Lists the supported zones for the given project."""
        # request type: cluster_messages.ListZonesRequest
        # get: "/v1/{name=projects/*}/zones"
        return cluster_messages.ListZonesResponse()

    def GetCluster(self, request):
        """Gets information about a particular cluster."""
        # request type: cluster_messages.GetClusterRequest
        # get: "/v1/{name=projects/*/zones/*/clusters/*}"
        return cluster_messages.Cluster()

    def ListClusters(self, request):
        """Lists clusters.

        Lists all clusters in the given project, along with any zones for which
        cluster information could not be retrieved.
        """
        # request type: cluster_messages.ListClustersRequest
        # get: "/v1/{name=projects/*}/aggregated/clusters"
        return cluster_messages.ListClustersResponse()

    def CreateCluster(self, request):
        """Creates a cluster.

        Creates a cluster and begins preparing it to begin serving. The returned
        cluster embeds as its "current_operation" a long-running operation which
        can be used to track the progress of turning up the new cluster.
        Immediately upon completion of this request:
         * The cluster will be readable via the API, with all requested attributes
           but no allocated resources.
        Until completion of the embedded operation:
         * Cancelling the operation will render the cluster immediately unreadable
           via the API.
         * All other attempts to modify or delete the cluster will be rejected.
        Upon completion of the embedded operation:
         * Billing for all successfully-allocated resources will begin (some types
           may have lower than the requested levels).
         * New tables can be created in the cluster.
         * The cluster's allocated resource levels will be readable via the API.
        The embedded operation's "metadata" field type is
        [CreateClusterMetadata][google.bigtable.admin.cluster.v1.CreateClusterMetadata] The embedded operation's "response" field type is
        [Cluster][google.bigtable.admin.cluster.v1.Cluster], if successful.
        """
        # request type: cluster_messages.CreateClusterRequest
        # post: "/v1/{name=projects/*/zones/*}/clusters"
        return cluster_messages.Cluster()

    def UpdateCluster(self, request):
        """Updates cluster.

        Updates a cluster, and begins allocating or releasing resources as
        requested. The returned cluster embeds as its "current_operation" a
        long-running operation which can be used to track the progress of updating
        the cluster.
        Immediately upon completion of this request:
         * For resource types where a decrease in the cluster's allocation has been
           requested, billing will be based on the newly-requested level.
        Until completion of the embedded operation:
         * Cancelling the operation will set its metadata's "cancelled_at_time",
           and begin restoring resources to their pre-request values. The operation
           is guaranteed to succeed at undoing all resource changes, after which
           point it will terminate with a CANCELLED status.
         * All other attempts to modify or delete the cluster will be rejected.
         * Reading the cluster via the API will continue to give the pre-request
           resource levels.
        Upon completion of the embedded operation:
         * Billing will begin for all successfully-allocated resources (some types
           may have lower than the requested levels).
         * All newly-reserved resources will be available for serving the cluster's
           tables.
         * The cluster's new resource levels will be readable via the API.
        [UpdateClusterMetadata][google.bigtable.admin.cluster.v1.UpdateClusterMetadata] The embedded operation's "response" field type is
        [Cluster][google.bigtable.admin.cluster.v1.Cluster], if successful.
        """
        # request type: cluster_messages.Cluster
        # put: "/v1/{name=projects/*/zones/*/clusters/*}"
        return cluster_messages.Cluster()

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
        # request type: cluster_messages.DeleteClusterRequest
        # delete: "/v1/{name=projects/*/zones/*/clusters/*}"
        return dependency_messages.Empty()

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
        # request type: cluster_messages.UndeleteClusterRequest
        # post: "/v1/{name=projects/*/zones/*/clusters/*}:undelete"
        return dependency_messages.Operation()
