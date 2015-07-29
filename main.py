import endpoints

import operations_service
import table_service


application = endpoints.api_server(
    [
        operations_service.Operations,
        table_service.BigtableTableService,
    ],
    restricted=False,
)
