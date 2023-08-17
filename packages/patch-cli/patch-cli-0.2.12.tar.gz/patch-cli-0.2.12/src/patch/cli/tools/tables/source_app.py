from textual.containers import Container
from textual.app import ComposeResult, App
from textual.widgets import Label

from patch.cli.tools.tables.components.container_panel import ContainerPanel
from patch.cli.tools.tables.components.panel_quota import PanelQuota
from patch.cli.tools.tables.components.panel_search import SearchContent
from patch.cli.tools.tables.components.panel_summary import PanelSummary
from patch.cli.tools.tables.components.panel_tabular_all_in import PanelTabularAllIn
from patch.cli.tools.tables.components.panel_tabular_positional import PanelTabularPositional
from patch.cli.tools.tables.components.panel_tabular_with_columns import PanelTabularWithColumns
from patch.cli.tools.tables.rows.columns_row_collection import ColumnsRowCollection
from patch.cli.tools.tables.rows.table_row_collection_quota_aware import TableRowCollectionQuotaAware
from patch.cli.tools.tables.rows.table_with_pk_row_collection import TableWithPkRowCollection
from patch.cli.tools.tables.source_data import SourceData
from patch.cli.tools.tables.state_manager import StateManager


class SourceApp(App[str]):
    CSS_PATH = "source_app.css"

    def __init__(self, **kwargs):
        self.meta = kwargs.pop('meta', None)
        self.client = kwargs.pop('client', None)
        self.source_data: SourceData = self.meta.source_data
        self.tables_quota_aware = TableRowCollectionQuotaAware(self.source_data.tables)
        self.state_mngr = None
        self.panel_search = SearchContent()
        self.panel_summary = PanelSummary()
        self.panel_quota = PanelQuota()
        self.all_tables = PanelTabularPositional.instance(
            'No tables to select', self.tables_quota_aware)
        self.selected_tables = PanelTabularWithColumns.instance(
            'Zero tables selected', TableWithPkRowCollection(self.source_data.selected_tables + self.source_data.obsolete_tables))
        self.primary_keys = PanelTabularAllIn.instance(
            'No Columns', ColumnsRowCollection([]))
        super().__init__()

    def compose(self) -> ComposeResult:
        self.panel_quota.initialize(self.source_data.quota, self.source_data.quota_used, self.tables_quota_aware)

        self.panel_summary.initialize(self.panel_quota)

        self.state_mngr = StateManager(
            self,
            self.panel_search, self.panel_summary, self.panel_quota,
            self.all_tables, self.selected_tables, self.primary_keys,
            self.tables_quota_aware, self.client)
        top_help_container = Container(
            Label(
                "[yellow]Select tables for your dataset by scrolling or searching. Then, select a unique column " +
                "as a Primary Key.\nIf none are unique, select multiple columns to form a composite key.[yellow]",
                id="help-text"),
            id="top-help-container"
        )
        bottom_help_container = Container(
            Label("[yellow]When you are finished, submit the dataset using CTRL+S. Press CTRL+C to cancel.[yellow]",
                  id="help-text"),
            id="bottom-help-container"
        )
        main_container = Container(
            ContainerPanel(self.panel_search, title='Search Tables'),
            ContainerPanel(self.panel_summary, title='Summary'),
            ContainerPanel(self.panel_quota, title='Quota'),
            ContainerPanel(self.all_tables, title='All Tables'),
            ContainerPanel(self.selected_tables, title='Selected Tables'),
            ContainerPanel(self.primary_keys, title='Primary Key Columns'),
            id="app-grid")

        yield top_help_container
        yield main_container
        yield bottom_help_container

    def startup(self):
        pass

    async def on_key(self, event):
        key = event.key
        await self.state_mngr.input_key(key)

    def action_prepare_to_quit(self):
        if self.panel_summary.is_all_set and self.panel_quota.submission_allowed:
            self.meta.source_data.selected_tables = self.selected_tables.get_rows()
            self.meta.source_data.is_ready = True
            self.exit('ok')

    async def on_mount(self) -> None:
        await self.state_mngr.initialize()
        # The syntax for a modifier key like this is not officially documented.
        # This is copying the syntax seen in Textual's code examples. You can
        # find an example for binding to 'ctrl+c' here:
        # https://github.com/Textualize/textual/blob/637635c/src/textual/app.py#L104
        quit_key = 'ctrl+s'

        self.bind(quit_key, 'prepare_to_quit')
