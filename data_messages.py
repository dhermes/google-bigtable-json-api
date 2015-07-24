from protorpc import messages


class Cell(messages.Message):
    # The cell's stored timestamp, which also uniquely identifies it within
    # its column.
    # Values are always expressed in microseconds, but individual tables may set
    # a coarser "granularity" to further restrict the allowed values. For
    # example, a table which specifies millisecond granularity will only allow
    # values of "timestamp_micros" which are multiples of 1000.
    timestamp_micros = messages.IntegerField(1, variant=messages.Variant.INT64)
    # The value stored in the cell.
    # May contain any byte string, including the empty string, up to 100MiB in
    # length.
    value = messages.BytesField(2)


class Column(messages.Message):
    # The unique key which identifies this column within its family. This is the
    # same key that's used to identify the column in, for example, a RowFilter
    # which sets its "column_qualifier_regex_filter" field.
    # May contain any byte string, including the empty string, up to 16kiB in
    # length.
    qualifier = messages.BytesField(1)
    # Must not be empty. Sorted in order of decreasing "timestamp_micros".
    cells = messages.MessageField(Cell, 2, repeated=True)


class Family(messages.Message):
    # The unique key which identifies this family within its row. This is the
    # same key that's used to identify the family in, for example, a RowFilter
    # which sets its "family_name_regex_filter" field.
    # Must match [-_.a-zA-Z0-9]+, except that AggregatingRowProcessors may
    # produce cells in a sentinel family with an empty name.
    # Must be no greater than 64 characters in length.
    name = messages.StringField(1)
    # Must not be empty. Sorted in order of increasing "qualifier".
    columns = messages.MessageField(Column, 2, repeated=True)


class Row(messages.Message):
    # The unique key which identifies this row within its table. This is the same
    # key that's used to identify the row in, for example, a MutateRowRequest.
    # May contain any non-empty byte string up to 16KiB in length.
    key = messages.BytesField(1)
    # May be empty, but only if the entire row is empty.
    # The mutual ordering of column families is not specified.
    families = messages.MessageField(Family, 2, repeated=True)


class RowRange(messages.Message):
    # Inclusive lower bound. If left empty, interpreted as the empty string.
    start_key = messages.BytesField(2)
    # Exclusive upper bound. If left empty, interpreted as infinity.
    end_key = messages.BytesField(3)


class ColumnRange(messages.Message):
    # The name of the column family within which this range falls.
    family_name = messages.StringField(1)

    # The column qualifier at which to start the range (within 'column_family').
    # If neither field is set, interpreted as the empty string, inclusive.
    # NOTE: oneof, start_qualifier{start_qualifier_inclusive,
    #                              start_qualifier_exclusive}

    # Used when giving an inclusive lower bound for the range.
    start_qualifier_inclusive = messages.BytesField(2)
    # Used when giving an exclusive lower bound for the range.
    start_qualifier_exclusive = messages.BytesField(3)

    # The column qualifier at which to end the range (within 'column_family').
    # If neither field is set, interpreted as the infinite string, exclusive.
    # NOTE: oneof, end_qualifier{end_qualifier_inclusive,
    #                            end_qualifier_exclusive}

    # Used when giving an inclusive upper bound for the range.
    end_qualifier_inclusive = messages.BytesField(4)
    # Used when giving an exclusive upper bound for the range.
    end_qualifier_exclusive = messages.BytesField(5)



class TimestampRange(messages.Message):
    # Inclusive lower bound. If left empty, interpreted as 0.
    start_timestamp_micros = messages.IntegerField(
        1, variant=messages.Variant.INT64)
    # Exclusive upper bound. If left empty, interpreted as infinity.
    end_timestamp_micros = messages.IntegerField(
        2, variant=messages.Variant.INT64)


class ValueRange(messages.Message):
    # The value at which to start the range.
    # If neither field is set, interpreted as the empty string, inclusive.
    # NOTE: oneof, start_value{start_value_inclusive,
    #                          start_value_exclusive}

    # Used when giving an inclusive lower bound for the range.
    start_value_inclusive = messages.BytesField(1)
    # Used when giving an exclusive lower bound for the range.
    start_value_exclusive = messages.BytesField(2)

    # The value at which to end the range.
    # If neither field is set, interpreted as the infinite string, exclusive.
    # NOTE: oneof, end_value{end_value_inclusive,
    #                        end_value_exclusive}

    # Used when giving an inclusive upper bound for the range.
    end_value_inclusive = messages.BytesField(3)
    # Used when giving an exclusive upper bound for the range.
    end_value_exclusive = messages.BytesField(4)


class RowFilter(messages.Message):

    # A RowFilter which sends rows through several RowFilters in sequence.
    class Chain(messages.Message):
        # The elements of "filters" are chained together to process the input row:
        # in row -> f(0) -> intermediate row -> f(1) -> ... -> f(N) -> out row
        # The full chain is executed atomically.
        filters = messages.MessageField('RowFilter', 1, repeated=True)

    # A RowFilter which sends each row to each of several component
    # RowFilters and interleaves the results.
    class Interleave(messages.Message):
        # The elements of "filters" all process a copy of the input row, and the
        # results are pooled, sorted, and combined into a single output row.
        # If multiple cells are produced with the same column and timestamp,
        # they will all appear in the output row in an unspecified mutual order.
        # Consider the following example, with three filters:
        #
        #                              input row
        #                                  |
        #        -----------------------------------------------------
        #        |                         |                         |
        #       f(0)                      f(1)                      f(2)
        #        |                         |                         |
        # 1: foo,bar,10,x             foo,bar,10,z              far,bar,7,a
        # 2: foo,blah,11,z            far,blah,5,x              far,blah,5,x
        #        |                         |                         |
        #        -----------------------------------------------------
        #                                  |
        # 1:                        foo,bar,10,z     # could have switched with #2
        # 2:                        foo,bar,10,x     # could have switched with #1
        # 3:                        foo,blah,11,z
        # 4:                        far,bar,7,a
        # 5:                        far,blah,5,x     # identical to #6
        # 6:                        far,blah,5,x     # identical to #5
        # All interleaved filters are executed atomically.
        filters = messages.MessageField('RowFilter', 1, repeated=True)

    # A RowFilter which evaluates one of two possible RowFilters, depending on
    # whether or not a predicate RowFilter outputs any cells from the input row.
    #
    # IMPORTANT NOTE: The predicate filter does not execute atomically with the
    # true and false filters, which may lead to inconsistent or unexpected
    # results. Additionally, Condition filters have poor performance, especially
    # when filters are set for the false condition.
    class Condition(messages.Message):
        # If "predicate_filter" outputs any cells, then "true_filter" will be
        # evaluated on the input row. Otherwise, "false_filter" will be evaluated.
        predicate_filter = messages.MessageField('RowFilter', 1)
        # The filter to apply to the input row if "predicate_filter" returns any
        # results. If not provided, no results will be returned in the true case.
        true_filter = messages.MessageField('RowFilter', 2)
        # The filter to apply to the input row if "predicate_filter" does not
        # return any results. If not provided, no results will be returned in the
        # false case.
        false_filter = messages.MessageField('RowFilter', 3)

    # Which of the possible RowFilter types to apply. If none are set, this
    # RowFilter returns all cells in the input row.
    # NOTE: oneof, filter{chain, interleave, condition, row_key_regex_filter,
    #                     row_sample_filter, family_name_regex_filter,
    #                     column_qualifier_regex_filter, column_range_filter,
    #                     timestamp_range_filter, value_regex_filter,
    #                     value_range_filter, cells_per_row_offset_filter,
    #                     cells_per_row_limit_filter,
    #                     cells_per_column_limit_filter,
    #                     strip_value_transformer}

    # Applies several RowFilters to the data in sequence, progressively
    # narrowing the results.
    chain = messages.MessageField(Chain, 1)
    # Applies several RowFilters to the data in parallel and combines the
    # results.
    interleave = messages.MessageField(Interleave, 2)
    # Applies one of two possible RowFilters to the data based on the output of
    # a predicate RowFilter.
    condition = messages.MessageField(Condition, 3)
    # Matches only cells from rows whose keys satisfy the given RE2 regex. In
    # other words, passes through the entire row when the key matches, and
    # otherwise produces an empty row.
    # Note that, since row keys can contain arbitrary bytes, the '\C' escape
    # sequence must be used if a true wildcard is desired. The '.' character
    # will not match the new line character '\n', which may be present in a
    # binary key.
    row_key_regex_filter = messages.BytesField(4)
    # Matches all cells from a row with probability p, and matches no cells
    # from the row with probability 1-p.
    row_sample_filter = messages.FloatField(14, variant=messages.Variant.DOUBLE)
    # Matches only cells from columns whose families satisfy the given RE2
    # regex. For technical reasons, the regex must not contain the ':'
    # character, even if it is not being used as a literal.
    # Note that, since column families cannot contain the new line character
    # '\n', it is sufficient to use '.' as a full wildcard when matching
    # column family names.
    family_name_regex_filter = messages.StringField(5)
    # Matches only cells from columns whose qualifiers satisfy the given RE2
    # regex.
    # Note that, since column qualifiers can contain arbitrary bytes, the '\C'
    # escape sequence must be used if a true wildcard is desired. The '.'
    # character will not match the new line character '\n', which may be
    # present in a binary qualifier.
    column_qualifier_regex_filter = messages.BytesField(6)
    # Matches only cells from columns within the given range.
    column_range_filter = messages.MessageField(ColumnRange, 7)
    # Matches only cells with timestamps within the given range.
    timestamp_range_filter = messages.MessageField(TimestampRange, 8)
    # Matches only cells with values that satisfy the given regular expression.
    # Note that, since cell values can contain arbitrary bytes, the '\C' escape
    # sequence must be used if a true wildcard is desired. The '.' character
    # will not match the new line character '\n', which may be present in a
    # binary value.
    value_regex_filter = messages.BytesField(9)
    # Matches only cells with values that fall within the given range.
    value_range_filter = messages.MessageField(ValueRange, 15)
    # Skips the first N cells of each row, matching all subsequent cells.
    cells_per_row_offset_filter = messages.IntegerField(
        10, variant=messages.Variant.INT32)
    # Matches only the first N cells of each row.
    cells_per_row_limit_filter = messages.IntegerField(
        11, variant=messages.Variant.INT32)
    # Matches only the most recent N cells within each column. For example,
    # if N=2, this filter would match column "foo:bar" at timestamps 10 and 9,
    # skip all earlier cells in "foo:bar", and then begin matching again in
    # column "foo:bar2".
    cells_per_column_limit_filter = messages.IntegerField(
        12, variant=messages.Variant.INT32)
    # Replaces each cell's value with the empty string.
    strip_value_transformer = messages.BooleanField(13)


class Mutation(messages.Message):

    # A Mutation which sets the value of the specified cell.
    class SetCell(messages.Message):
        # The name of the family into which new data should be written.
        # Must match [-_.a-zA-Z0-9]+
        family_name = messages.StringField(1)
        # The qualifier of the column into which new data should be written.
        # Can be any byte string, including the empty string.
        column_qualifier = messages.BytesField(2)
        # The timestamp of the cell into which new data should be written.
        # Use -1 for current Bigtable server time.
        # Otherwise, the client should set this value itself, noting that the
        # default value is a timestamp of zero if the field is left unspecified.
        # Values must match the "granularity" of the table (e.g. micros, millis).
        timestamp_micros = messages.IntegerField(
            3, variant=messages.Variant.INT64)
        # The value to be written into the specified cell.
        value = messages.BytesField(4)

    # A Mutation which deletes cells from the specified column, optionally
    # restricting the deletions to a given timestamp range.
    class DeleteFromColumn(messages.Message):
        # The name of the family from which cells should be deleted.
        # Must match [-_.a-zA-Z0-9]+
        family_name = messages.StringField(1)
        # The qualifier of the column from which cells should be deleted.
        # Can be any byte string, including the empty string.
        column_qualifier = messages.BytesField(2)
        # The range of timestamps within which cells should be deleted.
        time_range = messages.MessageField(TimestampRange, 3)

    # A Mutation which deletes all cells from the specified column family.
    class DeleteFromFamily(messages.Message):
        # The name of the family from which cells should be deleted.
        # Must match [-_.a-zA-Z0-9]+
        family_name = messages.StringField(1)

    # A Mutation which deletes all cells from the containing row.
    class DeleteFromRow(messages.Message):
        pass

    # Which of the possible Mutation types to apply.
    # NOTE: oneof, mutation{set_cell, delete_from_column,
    #                       delete_from_family, delete_from_row}

    # Set a cell's value.
    set_cell = messages.MessageField(SetCell, 1)
    # Deletes cells from a column.
    delete_from_column = messages.MessageField(DeleteFromColumn, 2)
    # Deletes cells from a column family.
    delete_from_family = messages.MessageField(DeleteFromFamily, 3)
    # Deletes cells from the entire row.
    delete_from_row = messages.MessageField(DeleteFromRow, 4)


class ReadModifyWriteRule(messages.Message):
    # The name of the family to which the read/modify/write should be applied.
    # Must match [-_.a-zA-Z0-9]+
    family_name = messages.StringField(1)
    # The qualifier of the column to which the read/modify/write should be
    # applied.
    # Can be any byte string, including the empty string.
    column_qualifier = messages.BytesField(2)

    # The rule used to determine the column's new latest value from its current
    # latest value.
    # NOTE: oneof, rule{append_value, increment_amount}

    # Rule specifying that "append_value" be appended to the existing value.
    # If the targeted cell is unset, it will be treated as containing the
    # empty string.
    append_value = messages.BytesField(3)
    # Rule specifying that "increment_amount" be added to the existing value.
    # If the targeted cell is unset, it will be treated as containing a zero.
    # Otherwise, the targeted cell must contain an 8-byte value (interpreted
    # as a 64-bit big-endian signed integer), or the entire request will fail.
    increment_amount = messages.IntegerField(
        4, variant=messages.Variant.INT64)


class ReadRowsRequest(messages.Message):
    # The unique name of the table from which to read.
    table_name = messages.StringField(1)

    # If neither row_key nor row_range is set, reads from all rows.
    # NOTE: oneof, target{row_key, row_range}

    # The key of a single row from which to read.
    row_key = messages.BytesField(2)
    # A range of rows from which to read.
    row_range = messages.MessageField(RowRange, 3)

    # The filter to apply to the contents of the specified row(s). If unset,
    # reads the entire table.
    filter = messages.MessageField(RowFilter, 5)
    # By default, rows are read sequentially, producing results which are
    # guaranteed to arrive in increasing row order. Setting
    # "allow_row_interleaving" to true allows multiple rows to be interleaved in
    # the response stream, which increases throughput but breaks this guarantee,
    # and may force the client to use more memory to buffer partially-received
    # rows.
    allow_row_interleaving = messages.BooleanField(6)
    # The read will terminate after committing to N rows' worth of results. The
    # default (zero) is to return all results.
    # Note that if "allow_row_interleaving" is set to true, partial results may
    # be returned for more than N rows. However, only N "commit_row" chunks will
    # be sent.
    num_rows_limit = messages.IntegerField(7, variant=messages.Variant.INT64)


class ReadRowsResponse(messages.Message):
    # Specifies a piece of a row's contents returned as part of the read
    # response stream.
    class Chunk(messages.Message):
        # NOTE: oneof, chunk{row_contents, reset_row, commit_row}

        # A subset of the data from a particular row. As long as no "reset_row"
        # is received in between, multiple "row_contents" from the same row are
        # from the same atomic view of that row, and will be received in the
        # expected family/column/timestamp order.
        row_contents = messages.MessageField(Family, 1)
        # Indicates that the client should drop all previous chunks for
        # "row_key", as it will be re-read from the beginning.
        reset_row = messages.BooleanField(2)
        # Indicates that the client can safely process all previous chunks for
        # "row_key", as its data has been fully read.
        commit_row = messages.BooleanField(3)

    # The key of the row for which we're receiving data.
    # Results will be received in increasing row key order, unless
    # "allow_row_interleaving" was specified in the request.
    row_key = messages.BytesField(1)
    # One or more chunks of the row specified by "row_key".
    chunks = messages.MessageField(Chunk, 2, repeated=True)


class SampleRowKeysRequest(messages.Message):
    # The unique name of the table from which to sample row keys.
    table_name = messages.StringField(1)


class SampleRowKeysResponse(messages.Message):
    # Sorted streamed sequence of sample row keys in the table. The table might
    # have contents before the first row key in the list and after the last one,
    # but a key containing the empty string indicates "end of table" and will be
    # the last response given, if present.
    # Note that row keys in this list may not have ever been written to or read
    # from, and users should therefore not make any assumptions about the row key
    # structure that are specific to their use case.
    row_key = messages.BytesField(1)
    # Approximate total storage space used by all rows in the table which precede
    # "row_key". Buffering the contents of all rows between two subsequent
    # samples would require space roughly equal to the difference in their
    # "offset_bytes" fields.
    offset_bytes = messages.IntegerField(2, variant=messages.Variant.INT64)


class MutateRowRequest(messages.Message):
    # The unique name of the table to which the mutation should be applied.
    table_name = messages.StringField(1)
    # The key of the row to which the mutation should be applied.
    row_key = messages.BytesField(2)
    # Changes to be atomically applied to the specified row. Entries are applied
    # in order, meaning that earlier mutations can be masked by later ones.
    # Must contain at least one entry and at most 100000.
    mutations = messages.MessageField(Mutation, 3, repeated=True)


class CheckAndMutateRowRequest(messages.Message):
    # The unique name of the table to which the conditional mutation should be
    # applied.
    table_name = messages.StringField(1)
    # The key of the row to which the conditional mutation should be applied.
    row_key = messages.BytesField(2)
    # The filter to be applied to the contents of the specified row. Depending
    # on whether or not any results are yielded, either "true_mutations" or
    # "false_mutations" will be executed. If unset, checks that the row contains
    # any values at all.
    predicate_filter = messages.MessageField(RowFilter, 6)
    # Changes to be atomically applied to the specified row if "predicate_filter"
    # yields at least one cell when applied to "row_key". Entries are applied in
    # order, meaning that earlier mutations can be masked by later ones.
    # Must contain at least one entry if "false_mutations" is empty, and at most
    # 100000.
    true_mutations = messages.MessageField(Mutation, 4, repeated=True)
    # Changes to be atomically applied to the specified row if "predicate_filter"
    # does not yield any cells when applied to "row_key". Entries are applied in
    # order, meaning that earlier mutations can be masked by later ones.
    # Must contain at least one entry if "true_mutations" is empty, and at most
    # 100000.
    false_mutations = messages.MessageField(Mutation, 5, repeated=True)


class CheckAndMutateRowResponse(messages.Message):
    # Whether or not the request's "predicate_filter" yielded any results for
    # the specified row.
    predicate_matched = messages.BooleanField(1)


class ReadModifyWriteRowRequest(messages.Message):
    # The unique name of the table to which the read/modify/write rules should be
    # applied.
    table_name = messages.StringField(1)
    # The key of the row to which the read/modify/write rules should be applied.
    row_key = messages.BytesField(2)
    # Rules specifying how the specified row's contents are to be transformed
    # into writes. Entries are applied in order, meaning that earlier rules will
    # affect the results of later ones.
    rules = messages.MessageField(ReadModifyWriteRule, 3, repeated=True)
