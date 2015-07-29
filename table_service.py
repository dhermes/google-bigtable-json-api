import endpoints

from protorpc import messages
from protorpc import remote

import dependency_messages
import table_messages


ADMIN_SCOPE = 'https://www.googleapis.com/auth/cloud-bigtable.admin'
CREATE_TABLE_CONTAINER = endpoints.ResourceContainer(
    table_messages.CreateTableRequest,
    name = messages.StringField(1, required=True),
)
LIST_TABLES_CONTAINER = endpoints.ResourceContainer(
    table_messages.ListTablesRequest,
    name = messages.StringField(1, required=True),
)
GET_TABLE_CONTAINER = endpoints.ResourceContainer(
    table_messages.GetTableRequest,
    name = messages.StringField(1, required=True),
)
DELETE_TABLE_CONTAINER = endpoints.ResourceContainer(
    table_messages.DeleteTableRequest,
    name = messages.StringField(1, required=True),
)
RENAME_TABLE_CONTAINER = endpoints.ResourceContainer(
    table_messages.RenameTableRequest,
    name = messages.StringField(1, required=True),
)
CREATE_COLUMN_FAMILY_CONTAINER = endpoints.ResourceContainer(
    table_messages.CreateColumnFamilyRequest,
    name = messages.StringField(1, required=True),
)

# Local version of ColumnFamily with no name property, to avoid
# collision in the ResourceContainer.
class ColumnFamily(messages.Message):
    gc_expression = messages.StringField(2)
    gc_rule = messages.MessageField(table_messages.GcRule, 3)

UPDATE_COLUMN_FAMILY_CONTAINER = endpoints.ResourceContainer(
    ColumnFamily,
    name = messages.StringField(1, required=True),
)
DELETE_COLUMN_FAMILY_CONTAINER = endpoints.ResourceContainer(
    table_messages.DeleteColumnFamilyRequest,
    name = messages.StringField(1, required=True),
)


@endpoints.api(name='bigtabletableadmin', version='v1',
               description='Bigtable Table API',
               hostname='bigtabletableadmin.googleapis.com',
               scopes=(ADMIN_SCOPE,))
class BigtableTableService(remote.Service):

    @endpoints.method(CREATE_TABLE_CONTAINER, table_messages.Table,
                      http_method='POST', name='tables.create',
                      path='{name}/tables')
    def CreateTable(self, request):
        """Create table.

        Creates a new table, to be served from a specified cluster.
        The table can be created with a full set of initial column families,
        specified in the request.
        """
        return table_messages.Table()

    @endpoints.method(LIST_TABLES_CONTAINER, table_messages.ListTablesResponse,
                      http_method='GET', name='tables.list',
                      path='{name}/tables')
    def ListTables(self, request):
        """Lists the names of all tables served from a specified cluster."""
        return table_messages.ListTablesResponse()

    @endpoints.method(GET_TABLE_CONTAINER, table_messages.Table,
                      http_method='GET', name='tables.get',
                      path='{name}')
    def GetTable(self, request):
        """Gets the schema of the specified table.

        This includes its column families.
        """
        return table_messages.Table()

    @endpoints.method(DELETE_TABLE_CONTAINER, dependency_messages.Empty,
                      http_method='DELETE', name='tables.delete',
                      path='{name}')
    def DeleteTable(self, request):
        """Permanently deletes a specified table and all of its data."""
        return dependency_messages.Empty()

    # Path should actually be {name}:rename but generator fails with
    # the colon, so we just replace it in the generated file.
    @endpoints.method(RENAME_TABLE_CONTAINER, dependency_messages.Empty,
                      http_method='POST', name='tables.rename',
                      path='{name}/rename')
    def RenameTable(self, request):
        """Changes the name of a specified table.

        Cannot be used to move tables between clusters, zones, or projects.
        """
        return dependency_messages.Empty()

    @endpoints.method(CREATE_COLUMN_FAMILY_CONTAINER,
                      table_messages.ColumnFamily,
                      http_method='POST', name='tables.columnfamilies.create',
                      path='{name}/columnFamilies')
    def CreateColumnFamily(self, request):
        """Creates a new column family within a specified table."""
        return table_messages.ColumnFamily()

    @endpoints.method(UPDATE_COLUMN_FAMILY_CONTAINER,
                      table_messages.ColumnFamily,
                      http_method='PUT', name='tables.columnfamilies.update',
                      path='{name}')
    def UpdateColumnFamily(self, request):
        """Changes the configuration of a specified column family."""
        return table_messages.ColumnFamily()

    # Path should actually be {name} but generator fails since DELETE:{name}
    # is repeated (though the value of name changes).
    @endpoints.method(DELETE_COLUMN_FAMILY_CONTAINER,
                      dependency_messages.Empty,
                      http_method='DELETE',
                      name='tables.columnfamilies.delete',
                      path='columnFamilies/{name}')
    def DeleteColumnFamily(self, request):
        """Permanently deletes a specified column family and all of its data."""
        return table_messages.dependency_messages.Empty()
