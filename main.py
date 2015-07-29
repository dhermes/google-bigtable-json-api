import endpoints

import table_service


application = endpoints.api_server(
    [
        table_service.BigtableTableService,
    ],
    restricted=False,
)
