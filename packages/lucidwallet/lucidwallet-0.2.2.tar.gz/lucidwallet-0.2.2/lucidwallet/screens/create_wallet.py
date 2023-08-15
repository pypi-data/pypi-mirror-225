from functools import partial

from fluxwallet.mnemonic import Mnemonic
from textual.app import ComposeResult
from textual.containers import Grid, Horizontal
from textual.message import Message
from textual.reactive import var
from textual.screen import Screen
from textual.validation import Length
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Select, Static
from textual import work


from lucidwallet.helpers import init_app
from lucidwallet.screens import MnemonicOverlay

languages = [
    "english",
    "spanish",
    "italian",
    "dutch",
    "french",
    "japanese",
    "chinese_simplified",
    "chinese_traditional",
]


# class Notification(Static):
#     def on_mount(self) -> None:
#         self.set_timer(3, self.remove)

#     def on_click(self) -> None:
#         self.remove()


class LanguagePicker(Widget):
    def __init__(self, language: str = "english"):
        self.language = language
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("Select Language")
        yield Select(
            [(x, x) for x in languages],
            prompt="Select language",
            value=self.language,
        )

    def reset(self) -> None:
        self.language = "english"
        select = self.query_one("Select", Select)
        select.value = "english"

    def on_select_changed(self, event: Select.Changed):
        self.language = event.value


class CreateWallet(Screen):
    BINDINGS = [
        (
            "escape",
            "reset_and_dismiss()",
            "home",
        ),
    ]

    nickname = var("")

    # class WalletLandingRequested(Message):
    #     def __init__(self, wallet: str, wallets: list[str], networks: list[str]):
    #         self.wallet = wallet
    #         self.wallets = wallets
    #         self.networks = networks
    #         super().__init__()

    def compose(self):
        yield Static("Create Wallet", id="create_wallet_title")
        yield LanguagePicker()
        yield Input(
            "",
            placeholder="Wallet nickname",
            id="nickname",
            validators=[Length(maximum=15, minimum=2)],
        )
        yield Grid(id="mnemonic_grid")
        yield Horizontal(
            Button("Cancel", variant="warning", id="wallet_create_cancel"),
            Button("Create", id="wallet_create", disabled=True),
            id="create_wallet_button_container",
        )

    def on_mount(self) -> None:
        self.wallet_names = []

        input = self.query_one("Input", Input)
        input.focus()

    def on_screen_resume(self) -> None:
        self.store_wallet_names()

    def on_input_changed(self, event: Input.Changed) -> None:
        if event.validation_result.failures:
            # self.mount(
            #     Notification(event.validation_result.failures, variant="failure")
            # )
            return

        if event.value:
            self.nickname = event.value

    def reset_all(self) -> None:
        self.nickname = ""
        input = self.query_one("Input", Input)
        input.value = ""
        lang_picker = self.query_one("LanguagePicker", LanguagePicker)
        lang_picker.reset()
        input.focus()

    @work(group="store_wallet_names", exclusive=True)
    async def store_wallet_names(self) -> None:
        app_data = await init_app()
        self.wallet_names = app_data.wallets

    async def on_button_pressed(self, event: Button.Pressed):
        event.stop()
        if event.button.id == "wallet_create":
            print("WALLET CREATE")
            if self.nickname in self.wallet_names:
                self.notify("Wallet name already exists")
                return

            lang_picker = self.query_one("LanguagePicker", LanguagePicker)
            mnemonic = Mnemonic(lang_picker.language).generate()

            self.app.push_screen(MnemonicOverlay(self.nickname, mnemonic))
            self.reset_all()
        else:
            self.action_reset_and_dismiss()

    def action_reset_and_dismiss(self) -> None:
        self.reset_all()
        if self.app.is_screen_installed("wallet_landing"):
            self.dismiss()
        else:
            self.app.switch_screen("welcome")

    def watch_nickname(self, new_value) -> None:
        create = self.query_one("#wallet_create", Button)

        if new_value:
            create.disabled = False
        else:
            create.disabled = True
