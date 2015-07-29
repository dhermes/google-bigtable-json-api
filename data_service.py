import endpoints

from protorpc import messages
from protorpc import remote

import data_messages
import dependency_messages
from scopes import DATA_SCOPE
from scopes import READ_ONLY_SCOPE


READ_ROWS_CONTAINER = endpoints.ResourceContainer(
    data_messages.ReadRowsRequest,
    table_name=messages.StringField(1, required=True),
)
SAMPLE_ROW_KEYS_CONTAINER = endpoints.ResourceContainer(
    data_messages.SampleRowKeysRequest,
    table_name=messages.StringField(1, required=True),
)
MUTATE_ROW_CONTAINER = endpoints.ResourceContainer(
    data_messages.MutateRowRequest,
    table_name=messages.StringField(1, required=True),
    row_key=messages.BytesField(2, required=True),
)
CHECK_AND_MUTATE_ROW_CONTAINER = endpoints.ResourceContainer(
    data_messages.CheckAndMutateRowRequest,
    table_name=messages.StringField(1, required=True),
    row_key=messages.BytesField(2, required=True),
)
READ_MODIFY_WRITE_ROW_CONTAINER = endpoints.ResourceContainer(
    data_messages.ReadModifyWriteRowRequest,
    table_name=messages.StringField(1, required=True),
    row_key=messages.BytesField(2, required=True),
)


@endpoints.api(name='bigtable', version='v1',
               description='Bigtable Data API',
               hostname='bigtable.googleapis.com',
               scopes=(DATA_SCOPE, READ_ONLY_SCOPE))
class BigtableService(remote.Service):

    # Path should actually be {table_name}/rows:read but generator fails
    # with the colon, so we just replace it in the generated file.
    @endpoints.method(READ_ROWS_CONTAINER, data_messages.ReadRowsResponse,
                      http_method='POST', name='rows.read',
                      path='{table_name}/rows/read')
    def ReadRows(self, request):
        """Read rows.

        NOTE: This is a "stream" method and not likely to work over HTTP/1.1.

        Streams back the contents of all requested rows, optionally applying
        the same Reader filter to each. Depending on their size, rows may be
        broken up across multiple responses, but atomicity of each row will
        still be preserved.
        """
        return data_messages.ReadRowsResponse()

    # Path should actually be {table_name}/rows:sampleKeys but generator fails
    # with the colon, so we just replace it in the generated file.
    @endpoints.method(SAMPLE_ROW_KEYS_CONTAINER,
                      data_messages.SampleRowKeysResponse,
                      http_method='GET', name='rows.samplekeys',
                      path='{table_name}/rows/sampleKeys')
    def SampleRowKeys(self, request):
        """Sample row keys.

        NOTE: This is a "stream" method and not likely to work over HTTP/1.1.

        Returns a sample of row keys in the table. The returned row keys will
        delimit contiguous sections of the table of approximately equal size,
        which can be used to break up the data for distributed tasks like
        mapreduces.
        """
        return data_messages.SampleRowKeysResponse()

    # Path should actually be {table_name}/rows/{row_key}:mutate but generator
    # fails with the colon, so we just replace it in the generated file.
    @endpoints.method(MUTATE_ROW_CONTAINER, dependency_messages.Empty,
                      http_method='POST', name='rows.mutate',
                      path='{table_name}/rows/{row_key}/mutate')
    def MutateRow(self, request):
        """Mutate row.

        Mutates a row atomically. Cells already present in the row are left
        unchanged unless explicitly changed by 'mutation'.
        """
        return dependency_messages.Empty()

    # Path should actually be {table_name}/rows/{row_key}:checkAndMutate but
    # generator fails with the colon, so we just replace it in the generated
    # file.
    @endpoints.method(CHECK_AND_MUTATE_ROW_CONTAINER,
                      data_messages.CheckAndMutateRowResponse,
                      http_method='POST', name='rows.checkandmutate',
                      path='{table_name}/rows/{row_key}/checkAndMutate')
    def CheckAndMutateRow(self, request):
        """Check and mutate row.

        Mutates a row atomically based on the output of a predicate
        Reader filter.
        """
        return data_messages.CheckAndMutateRowResponse()

    # Path should actually be {table_name}/rows/{row_key}:readModifyWrite but
    # generator fails with the colon, so we just replace it in the generated
    # file.
    @endpoints.method(READ_MODIFY_WRITE_ROW_CONTAINER, data_messages.Row,
                      http_method='POST', name='rows.readmodifywrite',
                      path='{table_name}/rows/{row_key}/readModifyWrite')
    def ReadModifyWriteRow(self, request):
        """Read, modify and write row.

        Modifies a row atomically, reading the latest existing timestamp/value
        from the specified columns and writing a new value at
        max(existing timestamp, current server time) based on pre-defined
        read/modify/write rules. Returns the new contents of all modified
        cells.
        """
        return data_messages.Row()
