from protorpc import messages

import dependency_messages


class Table(messages.Message):

    class TimestampGranularity(messages.Enum):
        MILLIS = 0

    # A unique identifier of the form
    # <cluster_name>/tables/[_a-zA-Z0-9][-_.a-zA-Z0-9]*
    name = messages.StringField(1)
    # If this Table is in the process of being created, the Operation used to
    # track its progress. As long as this operation is present, the Table will
    # not accept any Table Admin or Read/Write requests.
    current_operation = messages.MessageField(dependency_messages.Operation, 2)
    # The column families configured for this table, mapped by column family id.
    # NEEDED: map<string, ColumnFamily> column_families = 3;
    # The granularity (e.g. MILLIS, MICROS) at which timestamps are stored in
    # this table. Timestamps not matching the granularity will be rejected.
    # Cannot be changed once the table is created.
    granularity = messages.EnumField(TimestampGranularity, 4)


class GcRule(messages.Message):

    # A GcRule which deletes cells matching all of the given rules.
    class Intersection(messages.Message):
        # Only delete cells which would be deleted by every element of `rules`.
        rules = messages.MessageField('GcRule', 1, repeated=True)

    # A GcRule which deletes cells matching any of the given rules.
    class Union(messages.Message):
        # Delete cells which would be deleted by any element of `rules`.
        rules = messages.MessageField('GcRule', 1, repeated=True)

    # NOTE: oneof, rule{max_num_versions, max_age, intersection, union}

    # Delete all cells in a column except the most recent N.
    max_num_versions = messages.IntegerField(1, variant=messages.Variant.INT32)
    # Delete cells in a column older than the given age.
    max_age = messages.MessageField(dependency_messages.Duration, 2)
    # Delete cells that would be deleted by every nested rule.
    intersection = messages.MessageField(Intersection, 3)
    # Delete cells that would be deleted by any nested rule.
    union = messages.MessageField(Union, 4)


class ColumnFamily(messages.Message):
    # A unique identifier of the form <table_name>/families/[-_.a-zA-Z0-9]+
    # The last segment is the same as the "name" field in
    # google.bigtable.v1.Family.
    name = messages.StringField(1)
    # Garbage collection expression specified by the following grammar:
    #   GC = EXPR
    #      | "" ;
    #   EXPR = EXPR, "||", EXPR              (* lowest precedence *)
    #        | EXPR, "&&", EXPR
    #        | "(", EXPR, ")"                (* highest precedence *)
    #        | PROP ;
    #   PROP = "version() >", NUM32
    #        | "age() >", NUM64, [ UNIT ] ;
    #   NUM32 = non-zero-digit { digit } ;    (* # NUM32 <= 2^32 - 1 *)
    #   NUM64 = non-zero-digit { digit } ;    (* # NUM64 <= 2^63 - 1 *)
    #   UNIT =  "d" | "h" | "m"  (* d=days, h=hours, m=minutes, else micros *)
    # GC expressions can be up to 500 characters in length
    #
    # The different types of PROP are defined as follows:
    #   version() - cell index, counting from most recent and starting at 1
    #   age() - age of the cell (current time minus cell timestamp)
    #
    # Example: "version() > 3 || (age() > 3d && version() > 1)"
    #   drop cells beyond the most recent three, and drop cells older than three
    #   days unless they're the most recent cell in the row/column
    #
    # Garbage collection executes opportunistically in the background, and so
    # it's possible for reads to return a cell even if it matches the active GC
    # expression for its family.
    gc_expression = messages.StringField(2)
    # Garbage collection rule specified as a protobuf.
    # Supercedes `gc_expression`.
    # Garbage collection executes opportunistically in the background, and so
    # it's possible for reads to return a cell even if it matches the active GC
    # expression for its family.
    gc_rule = messages.MessageField(GcRule, 3)


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
