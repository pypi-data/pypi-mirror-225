import pyperclip
from fluxwallet.keys import HDKey
from fluxwallet.mnemonic import Mnemonic
from fluxwallet.wallet import Wallet
from textual import work
from textual.app import ComposeResult
from textual.containers import Center, Container, Grid, Horizontal
from textual.message import Message
from textual.screen import ModalScreen
from textual.widgets import Button, Static

import asyncio

from lucidwallet.helpers import init_app
from lucidwallet.screens import WalletLanding

MNEMONIC_TEXT = """Here is your new mnemonic. You will only get to see this once.
Write down, or copy to clipboard if you like to YOLO."""


class Notification(Static):
    def on_mount(self) -> None:
        self.set_timer(3, self.remove)

    def on_click(self) -> None:
        self.remove()


class MnemonicOverlay(ModalScreen[bool]):
    DEFAULT_CSS = """

    """

    class WalletCreated(Message):
        def __init__(self, wallet: Wallet) -> None:
            self.wallet = wallet

            super().__init__()

    def __init__(self, nickname: str, mnemonic: str) -> None:
        self.nickname = nickname
        self.mnemonic = mnemonic
        self.words = mnemonic.split(" ")

        self.hidden_words = [
            f"{index}: {'*' * len(word)}" for index, word in enumerate(self.words, 1)
        ]
        self.hidden_dom = [
            Static(f"{index}: {'*' * len(word)}")
            for index, word in enumerate(self.words, 1)
        ]

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Button("X", variant="error", id="exit"),
                id="mnemonic_exit",
            ),
            Center(Static(MNEMONIC_TEXT, id="mnemonic_notice")),
            Grid(*self.hidden_dom),
            Horizontal(
                Button("Reveal", variant="success", id="reveal"),
                Button("Copy", variant="warning", id="copy"),
                id="mnemonic_button_container",
            ),
        )

    async def on_mount(self) -> None:
        # self.query_one("#reveal", Button).focus()
        self.create_wallet()

    @work()
    async def create_wallet(self):
        # have already validated, but validate again
        seed = Mnemonic().to_seed(self.mnemonic).hex()
        hdkey = HDKey.from_seed(seed, network="flux")

        wallet = await Wallet.create(
            self.nickname,
            hdkey,
            network="flux",
        )

        if wallet:
            await wallet.new_key(network="bitcoin")
            app_data = await init_app()

            if not self.app.is_screen_installed("wallet_landing"):
                self.app.install_screen(
                    WalletLanding(
                        wallet,
                        app_data.networks,
                        app_data.wallets,
                    ),
                    name="wallet_landing",
                )

            self.post_message(self.WalletCreated(wallet))

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "reveal":
            dom_words = self.query("Grid>Static")
            if str(event.button.label) == "Reveal":
                event.button.label = "Hide"

                for index, (dom_item, word) in enumerate(zip(dom_words, self.words), 1):
                    dom_item.update(f"{index}: {word}")

            elif str(event.button.label) == "Hide":
                event.button.label = "Reveal"
                for dom_word, word in zip(dom_words, self.hidden_words):
                    dom_word.update(word)

        elif event.button.id == "copy":
            word_str = " ".join(self.words)

            try:
                self.app.config.copy_callback(word_str)
            except Exception:  # Fix
                self.notify("No clipboard available", severity="warning")
            else:
                self.notify("Mnemonic copied!")
        else:
            # this is ugly, only seems to be docker that's slow??
            while not self.app.is_screen_installed("wallet_landing"):
                await asyncio.sleep(0.05)

            self.app.switch_screen("wallet_landing")
