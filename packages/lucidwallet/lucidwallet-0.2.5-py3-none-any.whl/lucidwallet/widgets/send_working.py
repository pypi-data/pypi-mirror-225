from typing import Iterable

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal
from textual.messages import Message
from textual.reactive import reactive
from textual.validation import Function, Length, Number
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Select

# from .top_bar import TopBar

# address_book = {
#     "gravywallet": "t1XvGeQCfYMhfagYb3GmbKRajNEjpPRZHkB",
#     "Anwen": "t1CvGeCCfYMhfagYAba4Re3ajNEjpPRZJ74",
# }


class Send(Widget):
    DEFAULT_CSS = """
    Send {
        height: 100%;
        width: 1fr;
        min-width: 60;
        # align: center middle;
        outline: tall $primary;
        margin-top: 1;
        margin-bottom: 1;
        background: $panel;
    }
    Send>Horizontal>Input {
        width: 2fr;
        border: tall $primary;
        # margin: 1;
    }
    Send>Center {
        margin-left: 1;
        margin-top: 1;
    }
    #save {
        margin: 0;
        padding: 0;
        height: auto;
        min-width: 0;
        width: auto;
    }
    #save:focus {
        text-style: none;
        outline-top: tall black;
        background: black 80%;
    }
    #buttons {
        margin-left: 1;
        margin-top: 1;
        align: center middle;
    }
    #all_funds {
        margin: 0;
        padding-right: 1;
        margin-left: 1;
        outline-right: tall black;
        min-width: 0;
    }
    #all_funds:focus {
        text-style: none;
        outline-top: tall black;
        background: black 80%;
    }
    Send>Horizontal>Button {
        margin: 1;

    }
    Send>Horizontal>Select>SelectCurrent {
        border: tall $primary;
        max-height: 3;
    }
    Send>Horizontal>Select>SelectCurrent Static#label {
       overflow: hidden;
    }
    """

    sendto_address = reactive("")
    sendto_amount = reactive(0.0)
    send_enabled = reactive(False)
    save_enabled = reactive(False)

    class SendTxRequested(Message):
        def __init__(self, address: str, amount: float, message: str):
            self.address = address
            self.amount = amount
            self.message = message
            super().__init__()

    class MaxAmountRequested(Message):
        ...

    class AddressBookUpdateRequested(Message):
        def __init__(self, address: str):
            self.address = address
            super().__init__()

    def __init__(self, address_book: dict[str, str] = {}):
        self.address_book = address_book
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Input(
            placeholder="Address",
            id="address",
            # validators=[
            #     Function(function=self.validate_address_input),
            # ],
        )
