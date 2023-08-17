import re

from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Container, Horizontal
from textual.message import Message
from textual.reactive import var
from textual.screen import Screen
from textual.validation import Function
from textual.widgets import Button, Input, Select, Static


class ImportKeyToWallet(Screen[tuple[str, str] | None]):
    class KeyImportRequested(Message):
        def __init__(self, key: str) -> None:
            self.key = key
            super().__init__()

    DEFAULT_CSS = """
    """
    private_key = var("")

    def __init__(
        self, wallet_name: str, wallets: list, network_name: str, networks: list
    ):
        self.wallet_name = wallet_name
        self.wallets = wallets
        self.network_name = network_name
        self.networks = networks
        super().__init__()

    def on_mount(self) -> None:
        private_key = self.query_one("Input", Input)
        self.set_focus(private_key)

    def input_pk_validate(self, pk: str) -> bool:
        if pk == "":
            return True

        length = len(pk)
        regex = r"^[5KL][1-9A-HJ-NP-Za-km-z]{50,51}$"

        if length == 51 or length == 52:
            return bool(re.search(regex, pk))
        elif length == 64:
            try:
                int(pk, 16)
            except ValueError:
                return False
            else:
                return True
        else:
            return False

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Container(Button("X", variant="error", id="exit"), id="button_container"),
            Center(Static("Import Private Key"), id="import_key_title"),
            id="import_key_top_bar",
        )
        yield Horizontal(
            Input(
                None,
                placeholder="Paste or type your private key in WIF or Hex format",
                id="input_private_key",
                password=True,
                validators=[
                    Function(function=self.input_pk_validate),
                ],
            ),
            Button("\U0001F441", id="import_key_toggle"),
            id="private_key_container",
        )
        yield Horizontal(
            Select(
                id="wallet_id",
                options=[(x, x) for x in self.wallets],
                value=self.wallet_name,
                classes="import_key_select",
            ),
            Select(
                id="network_id",
                options=[(x, x) for x in self.networks],
                value=self.network_name,
                classes="import_key_select",
            ),
            id="import_key_dropdowns",
        )
        yield Horizontal(
            Button(
                "Clear",
                variant="warning",
                id="clear_private_key",
                classes="import_key_buttons",
            ),
            Button("Import", id="import_key_button", classes="import_key_buttons"),
            id="import_key_buttons_container",
        )

    @on(Input.Changed, "#input_private_key")
    def address_input_changed(self, event: Input.Changed) -> None:
        event.stop()

        if not event.validation_result.failures:
            self.private_key = event.value
        else:
            self.private_key = ""

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()

        if event.button.id == "import_key_toggle":
            self.toggle_key_view()

        if event.button.id == "clear_private_key":
            private_key = self.query_one("Input", Input)
            private_key.value = ""
            self.set_focus(private_key)
        if event.button.id == "import_key_button":
            wallet_select = self.query_one("#wallet_id", Select)
            network_select = self.query_one("#network_id", Select)
            self.dismiss((wallet_select.value, network_select.value, self.private_key))

        if event.button.id == "exit":
            self.dismiss()

    def toggle_key_view(self):
        private_key = self.query_one("Input", Input)

        if private_key.password:
            private_key.password = False
        else:
            private_key.password = True

    def watch_private_key(self, new_value: str) -> None:
        submit = self.query_one("#import_key_button", Button)

        if new_value:
            submit.disabled = False
        else:
            submit.disabled = True
