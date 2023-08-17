from __future__ import annotations

from typing import Iterable

from fluxwallet.keys import HDKey
from fluxwallet.mnemonic import Mnemonic as WalletMnemonic
from fluxwallet.wallet import Wallet, WalletError
from textual import on, work
from textual.app import ComposeResult, RenderResult
from textual.containers import Center, Container, Grid, Horizontal
from textual.events import Paste
from textual.message import Message
from textual.reactive import reactive, var
from textual.screen import Screen
from textual.validation import Length
from textual.widget import Widget
from textual.widgets import Button, Input, Label, Select

from lucidwallet.helpers import init_app
from lucidwallet.screens import WalletLanding

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


class MnemonicInput(Input):
    class MnemonicPaste(Message):
        def __init__(self, text: str):
            self.text = text
            super().__init__()

    def _on_paste(self, event: Paste):
        event.prevent_default()
        event.stop()
        self.post_message(self.MnemonicPaste(event.text))


class MnemonicWord(Widget, can_focus=True):
    value = reactive("")
    bip39_valid = var(False)
    wordlist = var([])

    class MnemonicWordFocused(Message):
        def __init__(self, word: MnemonicWord):
            self.word = word
            super().__init__()

    class MnemonicWordInvalidated(Message):
        def __init__(self, word: MnemonicWord):
            self.word = word
            super().__init__()

    def __init__(self, wordlist: list, *args, **kwargs):
        self._wordlist = wordlist
        super().__init__(*args, **kwargs)

    def on_mount(self):
        self.wordlist = self._wordlist

    def render(self) -> RenderResult:
        return self.value

    def on_focus(self):
        self.post_message(self.MnemonicWordFocused(self))

    def watch_value(self, new_value: str):
        if new_value in self.wordlist:
            self.bip39_valid = True
            self.add_class("-found")
        else:
            if self.bip39_valid == True:
                self.post_message(self.MnemonicWordInvalidated(self))

            self.bip39_valid = False
            self.remove_class("-found")

    def watch_wordlist(self, new_value: list):
        if self.value in new_value:
            self.bip39_valid = True
            self.add_class("-found")
        else:
            self.bip39_valid = False
            self.remove_class("-found")


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


class ImportFromMnemonic(Screen):
    DEFAULT_CSS = """
    """

    BINDINGS = [
        (
            "escape",
            "reset_and_dismiss()",
            "home",
        ),
    ]

    AUTO_FOCUS = "#nickname"

    selected_word: MnemonicWord | None = var(None)
    word_count = var(0)
    last_focused: MnemonicWord | None = var(None)
    nickname = var("")
    validated = var(False)
    submit_enabled = var(False)

    class WalletCreated(Message):
        def __init__(self, wallet: Wallet) -> None:
            self.wallet = wallet

            super().__init__()

    # class WalletLandingRequested(Message):
    #     def __init__(self, wallet: str, wallets: list[str], networks: list[str]):
    #         self.wallet = wallet
    #         self.wallets = wallets
    #         self.networks = networks
    #         super().__init__()

    def on_mount(self) -> None:
        self.wallet_names = []

    def on_screen_resume(self) -> None:
        self.store_wallet_names()

    def compose(self) -> ComposeResult:
        self.mnemonic = WalletMnemonic()

        yield LanguagePicker()
        yield Input(
            "",
            placeholder="Wallet nickname",
            id="nickname",
            validators=[Length(maximum=15)],
        )
        yield MnemonicInput(
            "", placeholder="Type mnemonic words or paste phrase", id="text"
        )
        yield Grid()
        yield Label(
            "Incorrect checksum, not a mnemonic phrase",
            id="wrong_checksum",
            classes="hidden",
        )
        yield Horizontal(
            Button("Reset Mnemonic", id="reset_button", variant="warning"),
            Button(
                "Import Wallet", id="import_button", variant="success", disabled=True
            ),
        )

    async def start_new_word(self, remove_input: bool = True) -> MnemonicWord:
        if remove_input:
            input = self.query_one("#text", Input)
            input.value = ""

        grid = self.query_one("Grid", Grid)
        self.word_count += 1
        new_word = MnemonicWord(
            self.mnemonic.wordlist(), classes="words", id=f"word_{self.word_count}"
        )
        await grid.mount(new_word)
        return new_word

    def valid_checksum(self, words: Iterable[MnemonicWord]) -> bool:
        words = " ".join([word.value for word in words])

        try:
            self.mnemonic.to_entropy(words)
        except ValueError:
            checksum = self.query_one("#wrong_checksum", Label)
            if checksum.has_class("hidden"):
                checksum.remove_class("hidden")

            return False
        else:
            return True

    def validate_words(self):
        words: Iterable[MnemonicWord] = self.query("MnemonicWord")
        import_button = self.query_one("#import_button", Button)

        if (
            len(words) == 12
            and all([x.bip39_valid for x in words])
            and self.valid_checksum(words)
        ):
            input = self.query_one("#text", Input)
            input.value = ""
            self.validated = True
            # so we can update after select does
            self.call_after_refresh(self.set_focus, import_button)

        else:
            self.validated = False
            invalid = (x for x in words if not x.bip39_valid)
            next_word = next(invalid, None)

            if next_word and next_word.value:
                self.selected_word = next_word
                self.set_focus(next_word)

    def action_focus_next(self):
        focus_chain = self.focus_chain
        if self.last_focused:
            self.last_focused = None
            self.selected_word.remove_class("-focused")
            selected = self.selected_word
        else:
            selected = self.focused

        current_index = self.focus_chain.index(selected)
        if current_index + 1 == len(focus_chain):
            self.set_focus(focus_chain[0])
        else:
            self.set_focus(focus_chain[current_index + 1])

    def action_focus_previous(self):
        focus_chain = self.focus_chain
        if self.last_focused:
            self.last_focused = None
            self.selected_word.remove_class("-focused")
            selected = self.selected_word
        else:
            selected = self.focused

        current_index = self.focus_chain.index(selected)
        if current_index == 0:
            self.set_focus(focus_chain[-1])
        else:
            self.set_focus(focus_chain[current_index - 1])

    def compute_submit_enabled(self):
        return True if self.validated and len(self.nickname) > 2 else False

    def watch_submit_enabled(self, new_value: bool):
        submit = self.query_one("#import_button")

        if new_value:
            submit.disabled = False
        else:
            submit.disabled = True

    @work(group="store_wallet_names", exclusive=True)
    async def store_wallet_names(self) -> None:
        app_data = await init_app()
        self.wallet_names = app_data.wallets

    @on(MnemonicWord.MnemonicWordFocused)
    def on_mnemonic_word_focused(self, event: MnemonicWord.MnemonicWordFocused):
        if self.selected_word:
            self.selected_word.remove_class("-focused")

        self.selected_word = event.word
        self.selected_word.add_class("-focused")

        words = self.query("MnemonicWord")
        last_word: MnemonicWord = words.last()

        if self.word_count < 12 and (not last_word.value or not last_word.bip39_valid):
            self.word_count -= 1
            last_word.remove()

        input = self.query_one("#text", Input)
        input.value = self.selected_word.value
        self.last_focused = self.selected_word
        self.set_focus(input)

    @on(MnemonicInput.MnemonicPaste)
    async def on_mnemonic_paste(self, event: MnemonicInput.MnemonicPaste) -> None:
        new_words = list(filter(None, event.text.split(" ")))

        if not self.selected_word:
            self.selected_word = await self.start_new_word()

        for index, word in enumerate(new_words, 1):
            self.selected_word.value = word

            if index < len(new_words):
                self.selected_word = await self.start_new_word()

        if len(new_words) < 12:
            self.selected_word = await self.start_new_word()

        self.validate_words()

    @on(MnemonicWord.MnemonicWordInvalidated)
    def on_mnemonic_word_invalidated(self) -> None:
        self.validated = False

    @on(Button.Pressed, "#reset_button")
    def reset_words(self) -> None:
        self.validated = False

        words: Iterable[MnemonicWord] = self.query("MnemonicWord")

        for word in words:
            word.remove()

        self.selected_word = None
        self.word_count = 0

        input = self.query_one("#text", Input)
        input.value = ""
        self.set_focus(input)

    def reset_all(self) -> None:
        self.reset_words()
        nickname = self.query_one("#nickname", Input)
        nickname.value = ""
        self.set_focus(nickname)

    @on(Input.Submitted, "#text")
    async def on_input_submitted(self, event: Input.Submitted):
        event.stop()

        if not event.value:
            return

        if self.selected_word.has_class("-focused"):
            self.selected_word.remove_class("-focused")

        if self.word_count < 12:
            self.selected_word = await self.start_new_word()
            return

        self.validate_words()

    @on(Input.Submitted, "#nickname")
    def on_nickname_submitted(self, event: Input.Submitted):
        if len(event.value) < 3:
            self.notify("Nickname must be at least 3 characters", serverity="error")

            return

        text = self.query_one("#text", Input)
        self.set_focus(text)

    def get_mnemonic_from_dom(self) -> str:
        words: Iterable[MnemonicWord] = self.query("MnemonicWord")
        return " ".join([word.value for word in words])

    @on(Button.Pressed, "#import_button")
    async def on_import(self, event: Button.Pressed):
        # only submit once
        event.button.disabled = True

        mnemonic = self.get_mnemonic_from_dom()
        # need to validate the mnemonic first, if someone just enters words willy nilly, willl get checksum error
        # ValueError: Invalid checksum 1000 for entropy b'\xc8\xcfum\x8dq9{\xafjLe\x97/\x14\x8b'
        if self.nickname in self.wallet_names:
            self.app.notify("Wallet name already exists")
            event.button.disabled = False
            return

        if await self.create_wallet(mnemonic):
            self.app.switch_screen("wallet_landing")
            self.reset_all()
        else:
            self.app.notify("Error creating Wallet")

    # @work(exclusive=True)
    async def create_wallet(self, mnemonic: str) -> bool:
        # have already validated, but validate again
        seed = self.mnemonic.to_seed(mnemonic).hex()
        hdkey = HDKey.from_seed(seed, network="flux")

        try:
            wallet = await Wallet.create(
                self.nickname,
                hdkey,
                network="flux",
            )
        except WalletError:
            return False

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
        return True

    @on(Input.Changed, "#nickname")
    def on_nickname_changed(self, event: Input.Changed):
        if event.validation_result.failures:
            self.notify(event.validation_result.failures, serverity="error")

            return

        if event.value:
            self.nickname = event.value

    @on(Input.Changed, "#text")
    async def on_input_changed(self, event: Input.Changed):
        event.stop()

        checksum = self.query_one("#wrong_checksum", Label)
        checksum.add_class("hidden")

        new_words = list(filter(None, event.value.split(" ")))
        if len(new_words) > 1:
            return

        words: Iterable[MnemonicWord] = self.query("MnemonicWord")
        if not event.value and all([x.bip39_valid for x in words]):
            return

        if not self.selected_word:
            self.selected_word = await self.start_new_word(remove_input=False)

        if event.value.endswith(" "):
            self.selected_word.value = event.value[:-1]
            if self.word_count == 12:
                event.input.value = event.value[:-1]
                event.input.action_end()
                return

            self.selected_word.remove_class("-focused")
            self.selected_word = await self.start_new_word()
            return

        self.selected_word.value = event.value

    def on_select_changed(self, event: Select.Changed) -> None:
        event.stop()

        self.mnemonic.change_language(event.value)
        words: Iterable[MnemonicWord] = self.query("MnemonicWord")
        for word in words:
            word.wordlist = self.mnemonic.wordlist()

        self.selected_word.remove_class("-focused")
        self.validate_words()

    def action_reset_and_dismiss(self) -> None:
        self.reset_all()
        if self.app.is_screen_installed("wallet_landing"):
            self.dismiss()
        else:
            self.app.switch_screen("welcome")

    # @on(WalletLandingRequested)
    # def wallet_landing_requested(self, event: WalletLandingRequested):
    #     if not self.app.is_screen_installed("wallet_landing"):
    #         self.app.install_screen(
    #             WalletLanding(
    #                 event.wallet, event.networks, event.wallets, full_scan_required=True
    #             ),
    #             name="wallet_landing",
    #         )
    #     self.app.switch_screen("wallet_landing")
    #     self.reset_all()


# seed = Mnemonic().to_seed(passphrase).hex()
# hdkey = HDKey.from_seed(seed, network=args.network)
# return Wallet.create(
#     wallet_name,
#     hdkey,
#     network=args.network,
#     witness_type=args.witness_type,
#     db_uri=db_uri,
# )
