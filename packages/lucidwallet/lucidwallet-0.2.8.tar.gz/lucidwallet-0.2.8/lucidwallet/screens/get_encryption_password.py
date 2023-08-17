from textual import on
from textual.app import ComposeResult
from textual.containers import Center, Horizontal
from textual.reactive import var
from textual.screen import Screen
from textual.validation import Length
from textual.widgets import Button, Input, Static, Switch


class EncryptionPassword(Screen[tuple[str, bool]]):
    DEFAULT_CSS = """
        EncryptionPassword {
            layers: base notification;
        }
    """

    password = var("")

    def __init__(self, message: str | None = None) -> None:
        self.message = message
        super().__init__()

    def on_mount(self) -> None:
        password = self.query_one("#input_encryption_password", Input)
        matcher = self.query_one("#password_matcher", Static)
        matcher.visible = False
        keychain_switch = self.query_one("Switch", Switch)

        if not self.app.config.keyring_available:
            keychain_switch.disabled = True
            keychain_switch.tooltip = (
                "No keychain found. See https://pypi.org/project/keyring"
            )

        if self.message:
            self.notify(self.message)

        self.set_focus(password)

    def compose(self) -> ComposeResult:
        yield Horizontal(
            # Container(Button("X", variant="error", id="exit"), id="button_container"),
            Center(
                Static("Database Encryption password"),
                id="get_encryption_password_title",
            ),
            id="encryption_password_top_bar",
        )
        yield Horizontal(
            Input(
                None,
                placeholder="Paste or type your encryption password here",
                id="input_encryption_password",
                password=True,
                validators=Length(minimum=3),
            ),
            Button(
                "\U0001F441", id="show_password_toggle", classes="encryption_toggle"
            ),
        )
        yield Horizontal(
            Input(
                None,
                placeholder="Confirm your encryption password here",
                id="repeat_encryption_password",
                password=True,
                validators=Length(minimum=3),
            ),
            Button(
                "\U0001F441", id="repeat_password_toggle", classes="encryption_toggle"
            ),
        )
        yield Center(Static("Passwords do not match", id="password_matcher"))
        yield Horizontal(
            Switch(value=False),
            Static("Store in Keychain", classes="label"),
            id="switch_container",
        )
        yield Horizontal(
            Button("Clear", variant="warning", id="clear_password"),
            Button("Set Password", id="set_password", disabled=True),
            id="get_encryption_buttons",
        )

    @on(Input.Changed, "#input_encryption_password")
    def password_input_changed(self, event: Input.Changed) -> None:
        event.stop()

        matcher = self.query_one("#password_matcher", Static)
        repeat = self.query_one("#repeat_encryption_password", Input)

        if event.value != repeat.value:
            matcher.visible = True
            self.password = ""
            matcher.update("Passwords do not match")
            if matcher.has_class("-matcher_success"):
                matcher.remove_class("-matcher_success")
        elif not event.value:
            matcher.visible = False
            self.password = ""
        else:
            self.password = event.value
            matcher.update("Passwords match")
            matcher.add_class("-matcher_success")

    @on(Input.Changed, "#repeat_encryption_password")
    def repeat_input_changed(self, event: Input.Changed) -> None:
        event.stop()

        matcher = self.query_one("#password_matcher", Static)
        input_password = self.query_one("#input_encryption_password", Input)

        if event.value != input_password.value:
            self.password = ""
            matcher.visible = True
            matcher.update("Passwords do not match")
            if matcher.has_class("-matcher_success"):
                matcher.remove_class("-matcher_success")
        else:
            matcher.update("Passwords match")
            matcher.add_class("-matcher_success")
            if not event.validation_result.failures:
                self.password = event.value

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()

        if event.button.id == "show_password_toggle":
            to_toggle = self.query_one("#input_encryption_password", Input)
            self.toggle_password_view(to_toggle)
        if event.button.id == "repeat_password_toggle":
            to_toggle = self.query_one("#repeat_encryption_password", Input)
            self.toggle_password_view(to_toggle)

        if event.button.id == "clear_password":
            password = self.query_one("#input_encryption_password", Input)
            repeat_password = self.query_one("#repeat_encryption_password", Input)
            password.value = ""
            repeat_password.value = ""
            self.set_focus(password)

        if event.button.id == "set_password":
            password = self.query_one("#input_encryption_password", Input)
            # self.app_info.last_used_wallet.db.set_encrypted_key(password.value)
            store_in_keychain = self.query_one("Switch", Switch)
            self.dismiss((password.value, store_in_keychain.value))
            # self.app.switch_screen(
            #     WalletLanding(
            #         self.app_info.last_used_wallet,
            #         self.app_info.wallets,
            #         self.app_info.networks,
            #     )
            # )

        # if event.button.id == "exit":
        #     self.dismiss(None)

    def toggle_password_view(self, input: Input):
        if input.password:
            input.password = False
        else:
            input.password = True

    def watch_password(self, new_value: str) -> None:
        print("watch password")
        print("new value", new_value)
        submit = self.query_one("#set_password", Button)

        if new_value:
            submit.disabled = False
        else:
            submit.disabled = True
