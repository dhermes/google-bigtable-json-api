import endpoints

import cluster_service
import data_service
import operations_service
import table_service


application = endpoints.api_server(
    [
        cluster_service.BigtableClusterService,
        data_service.BigtableService,
        operations_service.Operations,
        table_service.BigtableTableService,
    ],
    restricted=False,
)
