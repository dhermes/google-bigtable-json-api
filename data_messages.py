from protorpc import messages


class ReadRowsRequest(messages.Message):
    pass


class ReadRowsResponse(messages.Message):
    pass


class SampleRowKeysRequest(messages.Message):
    pass


class SampleRowKeysResponse(messages.Message):
    pass


class MutateRowRequest(messages.Message):
    pass


class CheckAndMutateRowRequest(messages.Message):
    pass


class CheckAndMutateRowResponse(messages.Message):
    pass


class ReadModifyWriteRowRequest(messages.Message):
    pass
