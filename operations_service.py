import endpoints

from protorpc import messages
from protorpc import remote

import dependency_messages
import operations_messages


GET_OPERATION_CONTAINER = endpoints.ResourceContainer(
    operations_messages.GetOperationRequest,
    name=messages.StringField(1, required=True),
)
CANCEL_OPERATION_CONTAINER = endpoints.ResourceContainer(
    operations_messages.CancelOperationRequest,
    name=messages.StringField(1, required=True),
)
DELETE_OPERATION_CONTAINER = endpoints.ResourceContainer(
    operations_messages.DeleteOperationRequest,
    name=messages.StringField(1, required=True),
)


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
@endpoints.api(name='operations', version='v1',
               description='Operations API')
class Operations(remote.Service):

    @endpoints.method(GET_OPERATION_CONTAINER, operations_messages.Operation,
                      http_method='GET', name='operations.get',
                      path='{name}')
    def GetOperation(self, request):
        """Get a long-running operation.

        Gets the latest state of a long-running operation.  Clients may use
        this method to poll the operation result at intervals as recommended
        by the API service.
        """
        return operations_messages.Operation()

    @endpoints.method(operations_messages.ListOperationsRequest,
                      operations_messages.ListOperationsResponse,
                      http_method='GET', name='operations.list',
                      path='operations')
    def ListOperations(self, request):
        """List long-running operations.

        Lists operations that match the specified filter in the request. If the
        server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.
        """
        return operations_messages.ListOperationsResponse()

    # Path should actually be {name}:cancel but generator fails with
    # the colon, so we just replace it in the generated file.
    @endpoints.method(CANCEL_OPERATION_CONTAINER, dependency_messages.Empty,
                      http_method='POST', name='operations.cancel',
                      path='{name}/cancel')
    def CancelOperation(self, request):
        """Cancel a long-running operation.

        Starts asynchronous cancellation on a long-running operation.  The
        server makes a best effort to cancel the operation, but success is not
        guaranteed.  If the server doesn't support this method, it returns
        `google.rpc.Code.UNIMPLEMENTED`.  Clients may use
        [Operations.GetOperation] or other methods to check whether the
        cancellation succeeded or the operation completed despite cancellation.
        """
        return dependency_messages.Empty()

    @endpoints.method(DELETE_OPERATION_CONTAINER, dependency_messages.Empty,
                      http_method='DELETE', name='operations.delete',
                      path='{name}')
    def DeleteOperation(self, request):
        """Delete a long-running operation.

        Deletes a long-running operation.  It indicates the client is no longer
        interested in the operation result. It does not cancel the operation.
        """
        return dependency_messages.Empty()
