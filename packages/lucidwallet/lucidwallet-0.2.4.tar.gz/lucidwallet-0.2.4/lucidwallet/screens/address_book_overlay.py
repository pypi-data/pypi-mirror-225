from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Label


class AddressBookOverlay(ModalScreen[bool]):
    DEFAULT_CSS = """
        AddressBookOverlay {
            align: center middle;
        }

        #dialog {
            grid-size: 2;
            grid-gutter: 1 2;
            grid-rows: 1fr 3;
            padding: 0 1;
            width: 60;
            height: 11;
            border: thick $background 80%;
            background: $surface;
        }

        #question {
            column-span: 2;
            height: 1fr;
            width: 1fr;
            content-align: center middle;
        }

        AddressBookOverlay>Grid>Button {
            width: 100%;
        }"""

    def __init__(self, nickname: str, address: str) -> None:
        self.nickname = nickname
        self.address = address

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Grid(
            Label(
                f"Are you sure you want to delete address book entry {self.nickname} with address: {self.address}",
                id="question",
            ),
            Button("Delete", variant="error", id="delete"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "delete":
            delete = True
        else:
            delete = False

        self.dismiss(delete)
