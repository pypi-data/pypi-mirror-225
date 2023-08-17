from patch.cli.tools.tables.components.panel_quota import PanelQuota
from patch.cli.tools.tables.components.panel_summary import PanelSummary
from patch.cli.tools.tables.components.panel_tabular_all_in import PanelTabularAllIn
from patch.cli.tools.tables.components.panel_tabular_appendable import PanelTabularAppendable


class PanelTabularWithColumns(PanelTabularAppendable):
    column_panel: PanelTabularAllIn = None
    summary_panel: PanelSummary = None
    quota_panel: PanelQuota = None

    def set_sub_panels(self, column_panel, summary_panel, quota_panel):
        self.column_panel = column_panel
        self.summary_panel = summary_panel
        self.quota_panel = quota_panel

    def current_row_changed(self):
        current_row = self.viewport.row_entry(self.cursor.remembered_row)
        if current_row is not None and current_row.columns:
            self.column_panel.replace_rows(current_row.columns)
        else:
            self.column_panel.replace_rows([])

    def get_rows_to_render(self):
        ready_count = 0
        data_list = super().get_rows_to_render()
        staged_size = 0
        nonexistent = 0
        for data_entry in data_list.filtered_entries:
            row = data_entry.value
            if row.has_pk():
                ready_count += 1
            if row.size_bytes:
                staged_size += row.size_bytes
            if not row.exists:
                nonexistent += 1
        self.summary_panel.set_selected(self.visible_rows_count() - nonexistent, ready_count)
        self.quota_panel.set_staged(staged_size)
        return data_list
