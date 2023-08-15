import pyperclip
from rich.text import Text
from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.events import Message
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import Button, Label, Select, Static


class Notification(Static):
    def on_mount(self) -> None:
        self.set_timer(3, self.remove)

    def on_click(self) -> None:
        self.remove()


class CopyLabel(Label):
    def action_copy_clipboard(self, text: str):
        try:
            self.app.config.copy_callback(text)
        except Exception:  # Fix
            self.notify("No clipboard available", severity="warning")
        else:
            self.post_message(self.Copied())

    class Copied(Message):
        ...


class TopBar(Widget):
    DEFAULT_CSS = """


    """

    balance = var(0.0)
    receive_address = var("")
    # selected_network = var("")
    # selected_wallet = var("")
    # wallets = var([])
    # networks = var([])

    class WalletSelected(Message):
        def __init__(self, wallet: str) -> None:
            self.wallet = wallet
            super().__init__()

    class NetworkSelected(Message):
        def __init__(self, network: str) -> None:
            self.network = network
            super().__init__()

    class SignMessageRequested(Message):
        ...

    class RescanAllRequested(Message):
        ...

    def __init__(
        self,
        balance: float = 0.0,
        selected_wallet: str = "",
        receive_address: str = "",
        wallets: list[str] | None = None,
        selected_network: str = "flux",
        networks: list[str] | None = None,
    ) -> None:
        self._balance = balance
        self._receive_address = receive_address

        self.selected_wallet = selected_wallet
        self.selected_network = selected_network
        self.wallets = wallets if wallets else []
        self.networks = networks if networks else []

        super().__init__()

    def on_mount(self):
        self.balance = self._balance
        self.receive_address = self._receive_address

        self.selected_wallet = self.selected_wallet
        self.selected_network = self.selected_network
        self.networks = self.networks
        self.wallets = self.wallets

        sign = self.query_one("#sign", Button)
        sign.tooltip = "Sign Message"
        rescan = self.query_one("#rescan_all", Button)
        rescan.tooltip = "Rescan all keys"

    def compose(self) -> ComposeResult:
        yield CopyLabel("", id="receive")
        yield Container(
            Label("", id="balance"),
            Select(
                id="topbar_network_id",
                options=[(x, x) for x in self.networks],
                value=self.selected_network,
            ),
        )
        yield Select(
            id="topbar_wallet_id",
            options=[(x, x) for x in self.wallets],
            value=self.selected_wallet,
            classes="wallet_select",
        )
        yield Button("\U0001F50E", id="rescan_all", classes="topbar_button")
        yield Button("\U0001F58B", id="sign", classes="topbar_button")

    def on_copy_label_copied(self):
        self.mount(Notification(Text("Copied!")))
        # self.notify("Receive address copied!", timeout=3)

    @on(Select.Changed, "#topbar_wallet_id")
    def on_wallet_changed(self, event: Select.Changed):
        event.stop()

        self.selected_wallet = event.value

        if event.value:
            self.post_message(self.WalletSelected(event.value))

    @on(Select.Changed, "#topbar_network_id")
    def on_network_changed(self, event: Select.Changed):
        event.stop()

        self.selected_network = event.value

        if event.value:
            self.post_message(self.NetworkSelected(event.value))

    def watch_balance(self, new_value: str) -> None:
        self._balance = new_value
        self.query_one("#balance", Label).update(f"Balance: { self._balance}")

    def watch_receive_address(self, new_value: str) -> None:
        self._receive_address = new_value
        receive = self.query_one("#receive", CopyLabel)
        # temporary until I sort out apis
        if self.selected_network != "flux":
            receive.update(f"Receive Address: {'ENABLING SOON!'.center(35, ' ')}")
        else:
            receive.update(
                f"Receive Address: [@click=copy_clipboard('{new_value}')]{new_value}[/]"
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "sign":
            self.post_message(self.SignMessageRequested())
        if event.button.id == "rescan_all":
            self.post_message(self.RescanAllRequested())

    def set_wallet_options(
        self,
        selected_wallet: str,
        selected_network: str,
        wallets: list[str],
        networks: list[str],
    ) -> None:
        self.selected_wallet = selected_wallet
        self.selected_network = selected_network
        self.wallets = wallets
        self.networks = networks

        wallet_select = self.query_one("#topbar_wallet_id", Select)
        network_select = self.query_one("#topbar_network_id", Select)

        wallet_select.set_options([(x, x) for x in wallets])
        wallet_select.value = selected_wallet

        network_select.set_options([(x, x) for x in networks])
        network_select.value = selected_network
