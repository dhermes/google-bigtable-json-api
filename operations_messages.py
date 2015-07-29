from protorpc import messages

import dependency_messages


# This resource represents a long-running operation that is the result of a
# network API call.
class Operation(messages.Message):
    """Defines google.longrunning.Operation"""
    # The name of the operation resource, which is only unique within the same
    # service that originally returns it.
    name = messages.StringField(1)
    # Some service-specific metadata associated with the operation.  It typically
    # contains progress information and common metadata such as create time.
    # Some services may not provide such metadata.  Any method that returns a
    # long-running operation should document the metadata type, if any.
    metadata = messages.MessageField(dependency_messages.Any, 2)
    # If the value is false, it means the operation is still in progress.
    # If true, the operation is completed and the `result` is available.
    done = messages.BooleanField(3)

    # NOTE: oneof, result{error, response}

    # The error result of the operation in case of failure.
    error = messages.MessageField(dependency_messages.Status, 4)
    # The normal response of the operation in case of success.  If the original
    # method returns no data on success, such as `Delete`, the response will be
    # `google.protobuf.Empty`.  If the original method is standard
    # `Get`/`Create`/`Update`, the response should be the resource.  For other
    # methods, the response should have the type `XxxResponse`, where `Xxx`
    # is the original method name.  For example, if the original method name
    # is `TakeSnapshot()`, the inferred response type will be
    # `TakeSnapshotResponse`.
    response = messages.MessageField(dependency_messages.Any, 5)


# The request message for [Operations.GetOperation][google.longrunning.Operations.GetOperation].
class GetOperationRequest(messages.Message):
    # The name of the operation resource.
    name = messages.StringField(1, required=True)


# The request message for [Operations.ListOperations][google.longrunning.Operations.ListOperations].
class ListOperationsRequest(messages.Message):
    # The name of the operation collection.
    name = messages.StringField(4)
    # The standard List filter.
    filter = messages.StringField(1)
    # The standard List page size.
    page_size = messages.IntegerField(2, variant=messages.Variant.INT32)
    # The standard List page token.
    page_token = messages.StringField(3)


# The response message for [Operations.ListOperations][google.longrunning.Operations.ListOperations].
class ListOperationsResponse(messages.Message):
    # A list of operations that match the specified filter in the request.
    operations = messages.MessageField(Operation, 1, repeated=True)
    # The standard List next-page token.
    next_page_token = messages.StringField(2)


# The request message for [Operations.CancelOperation][google.longrunning.Operations.CancelOperation].
class CancelOperationRequest(messages.Message):
    # The name of the operation resource to be cancelled.
    name = messages.StringField(1, required=True)


# The request message for [Operations.DeleteOperation][google.longrunning.Operations.DeleteOperation].
class DeleteOperationRequest(messages.Message):
    # The name of the operation resource to be deleted.
    name = messages.StringField(1, required=True)
