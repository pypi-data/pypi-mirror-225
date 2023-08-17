
from patch.cli.tools.tables.rows.table_row_collection import TableRowCollection


class TableRowCollectionQuotaAware(TableRowCollection):
    space_left_bytes: int

    def update_space_left(self, space_left_bytes):
        self.space_left_bytes = space_left_bytes
