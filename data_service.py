from protorpc import remote

import data_messages
import dependency_messages


class BigtableService(remote.Service):

    def ReadRows(self, request):
        """Read rows.

        Streams back the contents of all requested rows, optionally applying
        the same Reader filter to each. Depending on their size, rows may be
        broken up across multiple responses, but atomicity of each row will still
        be preserved.
        """
        # request type: data_messages.ReadRowsRequest
        # post: "/v1/{table_name=projects/*/zones/*/clusters/*/tables/*}/rows:read"
        # NOTE: This is a "stream" method
        return data_messages.ReadRowsResponse()

    def SampleRowKeys(self, request):
        """Sample row keys.

        Returns a sample of row keys in the table. The returned row keys will
        delimit contiguous sections of the table of approximately equal size,
        which can be used to break up the data for distributed tasks like
        mapreduces.
        """
        # request type: data_messages.SampleRowKeysRequest
        # get: "/v1/{table_name=projects/*/zones/*/clusters/*/tables/*}/rows:sampleKeys"
        # NOTE: This is a "stream" method
        return data_messages.SampleRowKeysResponse()

    def MutateRow(self, request):
        """Mutate row.

        Mutates a row atomically. Cells already present in the row are left
        unchanged unless explicitly changed by 'mutation'.
        """
        # request type: data_messages.MutateRowRequest
        # post: "/v1/{table_name=projects/*/zones/*/clusters/*/tables/*}/rows/{row_key}:mutate"
        return dependency_messages.Empty()

    def CheckAndMutateRow(self, request):
        """Check and mutate row.

        Mutates a row atomically based on the output of a predicate
        Reader filter.
        """
        # request type: data_messages.CheckAndMutateRowRequest
        # post: "/v1/{table_name=projects/*/zones/*/clusters/*/tables/*}/rows/{row_key}:checkAndMutate"
        return data_messages.CheckAndMutateRowResponse()

    def ReadModifyWriteRow(self, request):
        """Read, modify and write row.

        Modifies a row atomically, reading the latest existing timestamp/value from
        the specified columns and writing a new value at
        max(existing timestamp, current server time) based on pre-defined
        read/modify/write rules. Returns the new contents of all modified cells.
        """
        # request type: data_messages.ReadModifyWriteRowRequest
        # post: "/v1/{table_name=projects/*/zones/*/clusters/*/tables/*}/rows/{row_key}:readModifyWrite"
        return data_messages.Row()
