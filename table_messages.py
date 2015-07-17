from protorpc import messages


class CreateTableRequest(messages.Message):
    pass


class ListTablesRequest(messages.Message):
    pass


class ListTablesResponse(messages.Message):
    pass


class GetTableRequest(messages.Message):
    pass


class DeleteTableRequest(messages.Message):
    pass


class RenameTableRequest(messages.Message):
    pass


class CreateColumnFamilyRequest(messages.Message):
    pass


class DeleteColumnFamilyRequest(messages.Message):
    pass
