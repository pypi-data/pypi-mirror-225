from time import monotonic

from rich.text import Text
from textual.app import ComposeResult
from textual.events import MouseScrollDown, Focus, DescendantFocus
from textual.message import Message
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import DataTable, Label, Static
from textual.containers import Center

from lucidwallet.widgets import TxLoading


class TransactionHistory(Widget):
    HEADER = ("Out/In", "Date", "Time", "Value", "Units")
    DEFAULT_CSS = """
    # TransactionHistory {
    #     width: 1fr;
    #     margin-top: 1;
    #     margin-bottom: 1;
    #     background: $panel;
    #     outline-top: tall $primary;
    #     outline-left: tall $primary;
    #     outline-right: tall $primary;
    #     layers: base notifications;
    # }
    # .top {
    #     outline-top: tall $primary;
    #     width: 100%;
    #     height: 3;
    #     margin: 0 1 0 1;
    #     content-align: center middle;
    #     background: $panel;
    # }
    # .bottom {
    #     outline-bottom: tall $primary;
    #     width: 100%;
    #     height: 2;
    #     margin: 0 1 0 1;
    #     padding-bottom: 1;
    #     background: $panel;
    # }
    """

    rows = var([])

    class ScrollDataTable(DataTable):
        def _on_focus(self, event: Focus) -> None:
            # hack to stop scrolling on DataTable click
            event.prevent_default()
            # self.has_focus = True
            self.refresh()
            self.post_message(DescendantFocus())

    class ScrollCenter(Center):
        class LazyLoadRequested(Message):
            ...

        def __init__(self, *args, **kwargs) -> None:
            self.last_lazyload = 0.0
            super().__init__(*args, **kwargs)

        def on_mouse_scroll_down(self, event: MouseScrollDown) -> None:
            """Sends a lazy load request if we're near the bottom of the screen.
            Uses a 300ms debouce on lazy load requests

            Args:
                event (MouseScrollDown): unused scroll event
            """
            now = monotonic()
            if self.last_lazyload + 0.3 < now:
                self.last_lazyload = now

                if self.max_scroll_y == 0:
                    return

                match self.max_scroll_y:
                    case x if x < 50:
                        ratio = 0.4
                    case x if x >= 50 and x < 100:
                        ratio = 0.6
                    case x if x >= 100 < 200:
                        ratio = 0.75
                    case _:
                        ratio = 0.80

                if self.scroll_y / self.max_scroll_y > ratio:
                    self.post_message(self.LazyLoadRequested())

    class TxOverlayRequested(Message):
        def __init__(self, txid: str):
            self.txid = txid
            super().__init__()

    def __init__(self, rows: list[tuple[str | Text]]) -> None:
        self._rows = rows
        self.selected_row: str | None = None
        self.loading = False
        self.loading_widget = TxLoading(id="tx_loading")
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("Previous Transactions", classes="top")

        with self.ScrollCenter():
            yield self.ScrollDataTable()

        yield Label("", classes="bottom")

    def on_mount(self) -> None:
        table = self.query_one("ScrollDataTable", self.ScrollDataTable)

        for col in self.HEADER:
            table.add_column(col, key=col)

        self.rows = self._rows
        table.cursor_type = "row"

    def on_data_table_row_selected(self, event: DataTable.RowSelected):
        event.stop()

        if not event.row_key.value:
            return

        if self.selected_row != event.row_key.value:
            self.selected_row = event.row_key.value
            return

        self.post_message(self.TxOverlayRequested(event.row_key.value))

        # could add a timing element here? Like 100ms?
        # send message with txdata to parent

    def clear_table(self) -> None:
        self.rows = []

    async def set_loading(self) -> None:
        if not self.loading:
            self.loading = True
            self.disabled = True
            self.call_after_refresh(self.mount, self.loading_widget)

    def unset_loading(self) -> None:
        if self.loading:
            self.loading = False
            self.disabled = False
            self.call_after_refresh(self.loading_widget.remove)

    def scroll(self, y: float) -> None:
        scroll_center = self.query_one("ScrollCenter", self.ScrollCenter)
        self.call_after_refresh(scroll_center.scroll_to, y=y, animate=False)

    def update_date_time(self, txid: str, date: str, time: str) -> None:
        table = self.query_one("ScrollDataTable", self.ScrollDataTable)
        print("UPDATING TIME", time)
        table.update_cell(txid, "Date", date)
        table.update_cell(txid, "Time", time)

    def watch_rows(self, new_value: list[tuple]):
        table = self.query_one("ScrollDataTable", self.ScrollDataTable)
        self._rows = new_value

        if not self._rows:
            table.clear()

        for row in self._rows:
            table.add_row(*row[1:], key=row[0])

        table.sort("Date", "Time", reverse=True)
