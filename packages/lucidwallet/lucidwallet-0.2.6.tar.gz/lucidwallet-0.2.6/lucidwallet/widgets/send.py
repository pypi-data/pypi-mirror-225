from typing import Iterable

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Container, Horizontal
from textual.messages import Message
from textual.reactive import reactive
from textual.validation import Function, Length, Number
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Select, Static

# from .top_bar import TopBar

# address_book = {
#     "gravywallet": "t1XvGeQCfYMhfagYb3GmbKRajNEjpPRZHkB",
#     "Anwen": "t1CvGeCCfYMhfagYAba4Re3ajNEjpPRZJ74",
# }


class Send(Widget):
    DEFAULT_CSS = """
    # Send {
    #     height: 100%;
    #     width: 1fr;
    #     min-width: 60;
    #     # align: center middle;
    #     outline: tall $primary;
    #     margin-top: 1;
    #     margin-bottom: 1;
    #     background: $panel;
    #     layers: default notification;
    # }
    # Send>Input {
    #     margin: 1;
    # }
    # Send>Horizontal {
    #     margin-top: 1;
    #     margin-left: 1;
    #     height: 5;
    # }
    # Send>Horizontal>Select {
    #     width: 1fr;
    #     max-height: 3;
    #     margin-left: 2;
    # }
    # Send>Input {
    #     border: tall $primary;
    # }
    # Send>Horizontal>Input {
    #     width: 2fr;
    #     border: tall $primary;
    #     # margin: 1;
    # }
    # Send>Center {
    #     margin-left: 1;
    #     margin-top: 1;
    # }
    # #save {
    #     margin: 0;
    #     padding: 0;
    #     height: auto;
    #     min-width: 0;
    #     width: auto;
    # }
    # #save:focus {
    #     text-style: none;
    #     outline-top: tall black;
    #     background: black 80%;
    # }
    # #buttons {
    #     margin-left: 1;
    #     margin-top: 1;
    #     align: center middle;
    # }
    # #all_funds {
    #     margin: 0;
    #     padding-right: 1;
    #     margin-left: 1;
    #     outline-right: tall black;
    #     min-width: 0;
    # }
    # #all_funds:focus {
    #     text-style: none;
    #     outline-top: tall black;
    #     background: black 80%;
    # }
    # Send>Horizontal>Button {
    #     margin: 1;

    # }
    # Send>Horizontal>Select>SelectCurrent {
    #     border: tall $primary;
    #     max-height: 3;
    # }
    # Send>Horizontal>Select>SelectCurrent Static#label {
    #    overflow: hidden;
    # }
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
        self.disabled_overlay = Static("Coming soon", id="disabled_send_banner")
        self.disabled_mounted = False
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("Send coins", classes="top")
        yield Horizontal(
            Input(
                placeholder="Address",
                id="address",
                validators=[
                    Function(function=self.validate_address_input),
                ],
            ),
            Button("\U0001F4BE", id="save"),
            Select(
                id="address_book",
                options=[(x, x) for x in self.address_book],
                prompt="Address book",
            ),
        )
        yield Horizontal(
            Input(
                placeholder="Amount",
                validators=[
                    Function(function=self.validate_amount_input),
                ],
                id="amount",
            ),
            Button("Max", id="all_funds"),
        )
        yield Input(placeholder="Message", id="message")
        yield Horizontal(
            Button("Clear", variant="warning", id="clear"),
            Button("Send", disabled=True, id="send"),
            id="buttons",
        )
        yield Center(id="disabled_container")

    def validate_address_input(self, address: str) -> bool:
        if address == "":
            return True

        if address.startswith(("t1", "t3")) and len(address) == 35:
            self.sendto_address = address
            return True
        return False

    def validate_amount_input(self, amount: float | str) -> bool:
        if amount == "":
            return True

        validator = Number(minimum=0)
        return not bool(validator.validate(amount).failures)

    def on_mount(self):
        self.query_one("#address", Input).focus()

    def update_address_book(self, selected: str, address_book: dict[str, str]):
        self.address_book = address_book
        options_list = sorted([(x, x) for x in self.address_book.keys()])

        address_book_dom = self.query_one("#address_book", Select)
        address_book_dom.set_options(options_list)

        if selected:
            address_book_dom.value = selected

    def mount_disabled(self) -> None:
        if not self.disabled_mounted:
            self.disabled_mounted = True
            self.disabled = True
            container = self.query_one("#disabled_container", Center)
            container.mount(self.disabled_overlay)

    def unmount_disabled(self) -> None:
        if self.disabled_mounted:
            self.disabled_mounted = False
            self.disabled = False
            self.disabled_overlay.remove()

    @on(Input.Changed, "#address")
    def address_input_changed(self, event: Input.Changed) -> None:
        event.stop()

        if not event.validation_result.failures:
            self.sendto_address = event.value
        else:
            self.sendto_address = ""

    @on(Input.Changed, "#amount")
    def amount_input_changed(self, event: Input.Changed) -> None:
        event.stop()

        if event.value == "":
            self.sendto_amount = 0.0
            return

        if not event.validation_result.failures:
            self.sendto_amount = float(event.value)
        else:
            self.sendto_amount = 0.0

    @on(Select.Changed, "#address_book")
    def address_book_select_changed(self, event: Select.Changed) -> None:
        event.stop()

        if event.value:
            self.query_one("#address", Input).value = self.address_book[
                str(event.value)
            ]

    @on(Button.Pressed, "#send")
    def submit_transaction(self):
        message = self.query_one("#message", Input).value
        self.post_message(
            self.SendTxRequested(self.sendto_address, self.sendto_amount, message)
        )
        # self.clear_fields()
        # self.query_one("#address", Input).focus()

    @on(Button.Pressed, "#all_funds")
    def set_max_amount(self):
        self.post_message(self.MaxAmountRequested())

    @on(Button.Pressed, "#clear")
    def clear_fields(self):
        self.sendto_address = ""
        self.sendto_amount = 0.0

        inputs: Iterable[Input] = self.query("Input")
        for input in inputs:
            input.value = ""

        self.query_one("#address_book", Select).value = None
        self.query_one("#address", Input).focus()

    @on(Button.Pressed, "#save")
    def save_address(self):
        address = self.query_one("#address", Input).value
        self.post_message(self.AddressBookUpdateRequested(address))

    def compute_send_enabled(self) -> bool:
        return True if self.sendto_address and self.sendto_amount else False

    def compute_save_enabled(self) -> bool:
        return bool(self.sendto_address)

    def watch_send_enabled(self, new_value: bool) -> None:
        button = self.query_one("#send", Button)

        if new_value:
            button.disabled = False
            button.variant = "success"
        else:
            button.disabled = True
            button.variant = "default"

    def watch_save_enabled(self, new_value: bool) -> None:
        button = self.query_one("#save", Button)

        if new_value:
            button.disabled = False
        else:
            button.disabled = True
