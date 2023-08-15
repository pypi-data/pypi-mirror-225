import webbrowser

from fluxwallet.transactions import BaseTransaction
from fluxwallet.wallet import WalletTransaction
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, RichLog


class ExplorerLabel(Label):
    def action_open_explorer_link(self, txid: str):
        base = "https://explorer.runonflux.io/tx"
        webbrowser.open(f"{base}/{txid}")


class TxOverlay(ModalScreen):
    DEFAULT_CSS = """
    TxOverlay {
        align: center middle;
    }

    TxOverlay > Container {
        padding: 0 1;
        width: 90%;
        height: 90%;
        border: thick $background 80%;
        background: $surface;
    }
    TxOverlay > Container > Horizontal {
        border: tall $primary;
        height: 5;
        margin-bottom: 1;
        background: $primary-background;
    }

    #txid {
        margin-left: 2;
        height: 3;
        # height: 1fr;
        # width: 1fr;
        content-align: center middle;
        padding-left: 1;
        padding-right: 1;
    }

    #exit {
        margin-right: 2;
        min-width: 5;
        width: 5;
    }
    #button_container {
        align: right middle;
    }
    TxOverlay > Container > RichLog {
        padding: 2;
        border: tall $primary;
    }
    """

    BINDINGS = [
        ("ctrl+t", "app.toggle_dark", "Toggle Dark mode"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit"),
    ]

    def __init__(self, tx: WalletTransaction):
        self.wt = tx
        super().__init__()

    def compose(self) -> ComposeResult:
        label = f"View on explorer: [@click=open_explorer_link('{self.wt.tx.txid}')]{self.wt.tx.txid}[/]"

        yield Container(
            Horizontal(
                ExplorerLabel(label, id="txid"),
                Container(
                    Button("X", variant="error", id="exit"), id="button_container"
                ),
            ),
            RichLog(auto_scroll=False),
        )

    def on_mount(self):
        textlog = self.query_one("RichLog", RichLog)
        textlog.write(self.wt.tx.as_dict())
        textlog.write(" ")
        textlog.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()
