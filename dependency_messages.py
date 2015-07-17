from protorpc import messages


class Timestamp(messages.Message):
    """Defines google.protobuf.Timestamp."""
    # Represents seconds of UTC time since Unix epoch
    # 1970-01-01T00:00:00Z. Must be from from 0001-01-01T00:00:00Z to
    # 9999-12-31T23:59:59Z inclusive.
    seconds = messages.IntegerField(1, variant=messages.Variant.INT64)
    # Non-negative fractions of a second at nanosecond resolution. Negative
    # second values with fractions must still have non-negative nanos values
    # that count forward in time. Must be from 0 to 999,999,999
    # inclusive.
    nanos = messages.IntegerField(2, variant=messages.Variant.INT32)


class Any(messages.Message):
    """Defines google.protobuf.Any."""
    # A URL/resource name whose content describes the type of the
    # serialized message.
    #
    # For URLs which use the schema `http`, `https`, or no schema, the
    # following restrictions and interpretations apply:
    #
    # * If no schema is provided, `https` is assumed.
    # * The last segment of the URL's path must represent the fully
    #   qualified name of the type (as in `path/google.protobuf.Duration`).
    # * An HTTP GET on the URL must yield a [google.protobuf.Type][google.protobuf.Type]
    #   value in binary format, or produce an error.
    # * Applications are allowed to cache lookup results based on the
    #   URL, or have them precompiled into a binary to avoid any
    #   lookup. Therefore, binary compatibility needs to be preserved
    #   on changes to types. (Use versioned type names to manage
    #   breaking changes.)
    #
    # Schemas other than `http`, `https` (or the empty schema) might be
    # used with implementation specific semantics.
    #
    # Types originating from the `google.*` package
    # namespace should use `type.googleapis.com/full.type.name` (without
    # schema and path). A type service will eventually become available which
    # serves those URLs (projected Q2/15).
    type_url = messages.StringField(1)
    # Must be valid serialized data of the above specified type.
    value = messages.BytesField(2)


class Status(messages.Message):
    """Defines google.rpc.Status"""
    # The status code, which should be an enum value of [google.rpc.Code][google.rpc.Code].
    code = messages.IntegerField(1, variant=messages.Variant.INT32)
    # A developer-facing error message, which should be in English. Any
    # user-facing error message should be localized and sent in the
    # [google.rpc.Status.details][google.rpc.Status.details] field, or localized by the client.
    message = messages.StringField(2)
    # A list of messages that carry the error details.  There will be a
    # common set of message types for APIs to use.
    details = messages.MessageField(Any, 3, repeated=True)


class Operation(messages.Message):
    """Defines google.longrunning.Operation"""
    # The name of the operation resource, which is only unique within the same
    # service that originally returns it.
    name = messages.StringField(1)
    # Some service-specific metadata associated with the operation.  It typically
    # contains progress information and common metadata such as create time.
    # Some services may not provide such metadata.  Any method that returns a
    # long-running operation should document the metadata type, if any.
    metadata = messages.MessageField(Any, 2)
    # If the value is false, it means the operation is still in progress.
    # If true, the operation is completed and the `result` is available.
    done = messages.BooleanField(3)

    # NOTE: oneof, result{error, response}

    # The error result of the operation in case of failure.
    error = messages.MessageField(Status, 4)
    # The normal response of the operation in case of success.  If the original
    # method returns no data on success, such as `Delete`, the response will be
    # `google.protobuf.Empty`.  If the original method is standard
    # `Get`/`Create`/`Update`, the response should be the resource.  For other
    # methods, the response should have the type `XxxResponse`, where `Xxx`
    # is the original method name.  For example, if the original method name
    # is `TakeSnapshot()`, the inferred response type will be
    # `TakeSnapshotResponse`.
    response = messages.MessageField(Any, 5)
