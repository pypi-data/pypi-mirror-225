from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Static


class SendTxOverlay(ModalScreen[bool]):
    DEFAULT_CSS = """
    SendTxOverlay {
        align: center middle;
    }

    SendTxOverlay > Grid {
        grid-size: 2;
        grid-rows: 1fr 1fr 1fr 3;
        padding: 0 1;
        grid-gutter: 1 2;
        width: 50%;
        height: 80%;
        border: thick $background 80%;
        background: $surface;
    }

    .info {
        border: tall $primary;
        column-span: 2;
        height: 1fr;
        width: 1fr;
        content-align: left middle;
        padding-left: 1;
    }
    #message {
        content-align: left top
    }

    SendTxOverlay > Grid > Button {
        width: 100%;
    }
    """

    def __init__(self, address: str, amount: float, message: str) -> None:
        self.address = address
        self.amount = amount
        self.message = message

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Grid(
            Static(f"Send to: {self.address}", classes="info"),
            Static(f"Amount to send: {str(self.amount)} FLUX", classes="info"),
            Static(f"Message: {self.message}", classes="info", id="message"),
            Button("Confirm", variant="success", id="confirm"),
            Button("Discard", variant="error", id="discard"),
        )

    def on_mount(self) -> None:
        self.query_one("#discard", Button).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        send = True if event.button.id == "confirm" else False
        self.dismiss(send)
