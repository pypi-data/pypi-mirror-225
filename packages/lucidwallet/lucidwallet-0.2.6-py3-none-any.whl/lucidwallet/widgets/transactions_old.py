from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Center
from textual.message import Message
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import DataTable, Label


class TransactionHistory(Widget):
    HEADER = ("Out/In", "Date", "Time", "Value", "Units")
    DEFAULT_CSS = """
    TransactionHistory {
        height: 100%;
        width: 1fr;
        margin-top: 1;
        margin-bottom: 1;
        background: $panel;
        outline-top: tall $primary;
        outline-left: tall $primary;
        outline-right: tall $primary;
    }
    .top {
        outline-top: tall $primary;
        width: 100%;
        height: 3;
        margin: 0 1 0 1;
        content-align: center middle;
        background: $panel;
    }
    .bottom {
        outline-bottom: tall $primary;
        width: 100%;
        height: 2;
        margin: 0 1 0 1;
        padding-bottom: 1;
        background: $panel;
    }
    TransactionHistory>Center {
        margin-left: 1;
        overflow: auto;
        height: 1fr;
        scrollbar-gutter: stable;

    }
    TransactionHistory>Center>DataTable {
        background: $panel;
        height: auto;
        width: auto;
    }
    """

    rows = var([])

    class TxOverlayRequested(Message):
        def __init__(self, txid: str):
            self.txid = txid
            super().__init__()

    def __init__(self, rows: list[tuple[str | Text]]) -> None:
        self._rows = rows
        self.selected_row: str | None = None
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("Previous Transactions", classes="top")
        yield Center(DataTable())
        yield Label("", classes="bottom")

    def on_mount(self) -> None:
        table = self.query_one("DataTable", DataTable)

        for col in self.HEADER:
            table.add_column(col, key=col)

        self.rows = self._rows
        table.cursor_type = "row"

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        print("ROW SELECTED")
        event.stop()

        if not event.row_key.value:
            return

        if self.selected_row != event.row_key.value:
            self.selected_row = event.row_key.value
            return

        self.post_message(self.TxOverlayRequested(event.row_key.value))

        # could add a timing element here? Like 100ms?
        # send message with txdata to parent

    def watch_rows(self, new_value: list[tuple]):
        table = self.query_one("DataTable", DataTable)

        self._rows = new_value

        if not self._rows:
            table.clear()

        for row in self._rows:
            table.add_row(*row[1:], key=row[0])

        table.sort("Date", "Time", reverse=True)
        # table.cursor_coordinate = Coordinate(2, 0)
