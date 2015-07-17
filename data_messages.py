from protorpc import messages


class Row(messages.Message):
    pass


class Family(messages.Message):
    pass


class Column(messages.Message):
    pass


class Cell(messages.Message):
    pass


class RowRange(messages.Message):
    pass


class ColumnRange(messages.Message):
    pass


class TimestampRange(messages.Message):
    pass


class ValueRange(messages.Message):
    pass


class RowFilter(messages.Message):
    pass


class Mutation(messages.Message):
    pass


class ReadModifyWriteRule(messages.Message):
    pass


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
