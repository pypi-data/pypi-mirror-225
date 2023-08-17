import webbrowser

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static


class ExplorerLabel(Label):
    def action_open_explorer_link(self, txid: str):
        base = "https://explorer.runonflux.io/tx"
        webbrowser.open(f"{base}/{txid}")


class TxSentOverlay(ModalScreen):
    def __init__(self, txid: str):
        self.txid = txid
        super().__init__()

    def on_mount(self) -> None:
        self.set_focus(None)

    def compose(self) -> ComposeResult:
        label = f"View on explorer: [@click=open_explorer_link('{self.txid}')]{self.txid}[/]"
        yield Container(
            Horizontal(
                ExplorerLabel(label, id="txid"),
                Container(
                    Button("X", variant="error", id="exit"), id="button_container"
                ),
            ),
            Static("Transaction Sent!", id="sent_message"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()
