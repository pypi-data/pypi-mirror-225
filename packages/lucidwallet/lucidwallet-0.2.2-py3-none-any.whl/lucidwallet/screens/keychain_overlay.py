import webbrowser

from fluxwallet.transactions import BaseTransaction
from fluxwallet.wallet import WalletTransaction
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, Grid, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class KeychainOverlay(ModalScreen[bool]):
    DEFAULT_CSS = """
        KeychainOverlay {
            align: center middle;
        }

        KeychainOverlay #dialog {
            grid-size: 2;
            grid-gutter: 1 2;
            grid-rows: 1fr 3;
            padding: 0 1;
            width: 60;
            height: 11;
            border: thick $background 80%;
            background: $surface;
        }

        KeychainOverlay #question {
            column-span: 2;
            height: 1fr;
            width: 1fr;
            content-align: center middle;
        }

        KeychainOverlay Button {
            width: 100%;
        }
    """

    BINDINGS = [
        ("ctrl+t", "app.toggle_dark", "Toggle Dark mode"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(
                "Do you want to store password in Keychain if available?", id="question"
            ),
            Button("Yes", variant="error", id="yes"),
            Button("No", variant="primary", id="no"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "no":
            self.dismiss(False)
        else:
            self.dismiss(True)
