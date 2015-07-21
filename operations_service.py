from protorpc import remote

import dependency_messages
import operations_messages


# Manages long-running operations with an API service.
#
# When an API method normally takes long time to complete, it can be designed
# to return [Operation][google.longrunning.Operation] to the client, and the client can use this
# interface to receive the real response asynchronously by polling the
# operation resource, or using `google.watcher.v1.Watcher` interface to watch
# the response, or pass the operation resource to another API (such as Google
# Cloud Pub/Sub API) to receive the response.  Any API service that returns
# long-running operations should implement the `Operations` interface so
# developers can have a consistent client experience.
class Operations(remote.Service):

    def GetOperation(self, request):
        """Get a long-running operation.

        Gets the latest state of a long-running operation.  Clients may use this
        method to poll the operation result at intervals as recommended by the API
        service.
        """
        # request_type: operations_messages.GetOperationRequest
        # get: "/v1/{name=operations/**}"
        return operations_messages.Operation()

    def ListOperations(self, request):
        """List long-running operations.

        Lists operations that match the specified filter in the request. If the
        server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.
        """
        # request_type: operations_messages.ListOperationsRequest
        # get: "/v1/{name=operations}"
        return operations_messages.ListOperationsResponse()

    def CancelOperation(self, request):
        """Cancel a long-running operation.

        Starts asynchronous cancellation on a long-running operation.  The server
        makes a best effort to cancel the operation, but success is not
        guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.  Clients may use
        [Operations.GetOperation] or other methods to check whether the
        cancellation succeeded or the operation completed despite cancellation.
        """
        # request_type: operations_messages.CancelOperationRequest
        # post: "/v1/{name=operations/**}:cancel"
        return dependency_messages.Empty()

    def DeleteOperation(self, request):
        """Delete a long-running operation.

        Deletes a long-running operation.  It indicates the client is no longer
        interested in the operation result. It does not cancel the operation.
        """
        # request_type: operations_messages.DeleteOperationRequest
        # delete: "/v1/{name=operations/**}"
        return dependency_messages.Empty()
