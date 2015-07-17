from protorpc import remote

import dependency_messages
import table_messages


class BigtableTableService(remote.Service):

    def CreateTable(self, request):
        """Create table.

        Creates a new table, to be served from a specified cluster.
        The table can be created with a full set of initial column families,
        specified in the request.
        """
        # request_type: table_messages.CreateTableRequest
        # post: "/v1/{name=projects/*/zones/*/clusters/*}/tables"
        return table_messages.Table()

    def ListTables(self, request):
        """Lists the names of all tables served from a specified cluster."""
        # request_type: table_messages.ListTablesRequest
        # get: "/v1/{name=projects/*/zones/*/clusters/*}/tables"
        return table_messages.ListTablesResponse()

    def GetTable(self, request):
        """Gets the schema of the specified table, including its column families."""
        # request_type: table_messages.GetTableRequest
        # get: "/v1/{name=projects/*/zones/*/clusters/*/tables/*}"
        return table_messages.Table()

    def DeleteTable(self, request):
        """Permanently deletes a specified table and all of its data."""
        # request_type: table_messages.DeleteTableRequest
        # delete: "/v1/{name=projects/*/zones/*/clusters/*/tables/*}"
        return table_messages.dependency_messages.Empty()

    def RenameTable(self, request):
        """Changes the name of a specified table.

        Cannot be used to move tables between clusters, zones, or projects.
        """
        # request_type: table_messages.RenameTableRequest
        # post: "/v1/{name=projects/*/zones/*/clusters/*/tables/*}:rename"
        return table_messages.dependency_messages.Empty()

    def CreateColumnFamily(self, request):
        """Creates a new column family within a specified table."""
        # request_type: table_messages.CreateColumnFamilyRequest
        # post: "/v1/{name=projects/*/zones/*/clusters/*/tables/*}/columnFamilies"
        return table_messages.ColumnFamily()

    def UpdateColumnFamily(self, request):
        """Changes the configuration of a specified column family."""
        # request_type: table_messages.ColumnFamily
        # put: "/v1/{name=projects/*/zones/*/clusters/*/tables/*/columnFamilies/*}"
        return table_messages.ColumnFamily()

    def DeleteColumnFamily(self, request):
        """Permanently deletes a specified column family and all of its data."""
        # request_type: table_messages.DeleteColumnFamilyRequest
        # delete: "/v1/{name=projects/*/zones/*/clusters/*/tables/*/columnFamilies/*}"
        return table_messages.dependency_messages.Empty()
