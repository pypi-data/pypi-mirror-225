import hashlib

import keyring
from fluxwallet.db_new import Db
from textual.app import ComposeResult
from textual.containers import Center, Horizontal
from textual.screen import Screen
from textual.widgets import Button, Label

from lucidwallet.screens import EncryptionPassword

MESSAGE = """
Welcome to LucidWallet! This looks like your first time here... lets get you setup.

* BIP39 and BIP44 compliant.
* Supports multiple currencies. (Soon)

"""


class FirstRun(Screen):
    BINDINGS = [
        (
            "a",
            "add_weiner()",
            "Add Weiner",
        ),
    ]
    AUTO_FOCUS = ""

    def compose(self) -> ComposeResult:
        yield Center(
            Label(
                MESSAGE,
                id="first_time",
            )
        )
        yield Center(
            Label(
                "Password encrypt database? (You can change this later)",
                id="encrypt_db_label",
            ),
            id="label_container",
        )
        yield Horizontal(
            Button("Yes", id="encrypt_db", variant="primary"),
            Button("Skip", id="no_encrypt_db", variant="warning"),
            classes="horizontal_center",
        )
        yield Horizontal(
            Button(
                "Create Wallet", id="create_wallet", variant="primary", disabled=True
            ),
            Button(
                "Import from Mnemonic",
                id="from_mnemonic",
                variant="primary",
                disabled=True,
            ),
            Button(
                "Import from Private key (xpriv)",
                id="from_xpriv",
                variant="primary",
                disabled=True,
            ),
            # Button(
            #     "Set Db URI",
            #     id="select_database",
            #     variant="primary",
            # ),
            classes="horizontal_center",
        )
        # yield Footer()

    def keychain_callback(self, password: str, store_in_chain: bool) -> None:
        if not store_in_chain:
            return

        keyring.set_password("fluxwallet", "fluxwallet_user", password)

    async def on_encryption_password_set(self, result: tuple[str, bool]):
        password, store_in_keychain = result

        hashed = hashlib.sha256(bytes(password, "utf8")).hexdigest()

        # callback = partial(self.keychain_callback, hashed)
        # self.app.push_screen(KeychainOverlay(), callback)

        if store_in_keychain:
            keyring.set_password("fluxwallet", "fluxwallet_user", hashed)

        db = Db()
        await db.set_db_encryption(hashed)

        print("PASSWORD SET", hashed)

    def remove_encrypt_buttons(self) -> None:
        buttons: list[Button] = self.query("Button")
        label_container = self.query_one("#label_container", Center)
        label_container.remove()
        for button in buttons:
            if button.id in ["no_encrypt_db", "encrypt_db"]:
                button.remove()
                # button.disabled = True
            elif button.id in ["create_wallet", "from_mnemonic", "from_xpriv"]:
                button.disabled = False

    def on_button_pressed(self, event: Button.Pressed):
        event.stop()
        self.set_focus(None)

        # if event.button.id == "create_wallet":
        #     self.app.switch_screen("create_wallet")
        if event.button.id == "from_mnemonic":
            self.app.switch_screen("from_mnemonic")
        if event.button.id == "encrypt_db":
            self.app.push_screen(EncryptionPassword(), self.on_encryption_password_set)
            self.remove_encrypt_buttons()
        if event.button.id == "create_wallet":
            self.app.switch_screen("create_wallet")

        if event.button.id == "no_encrypt_db":
            self.remove_encrypt_buttons()

        # self.set_focus(None)
