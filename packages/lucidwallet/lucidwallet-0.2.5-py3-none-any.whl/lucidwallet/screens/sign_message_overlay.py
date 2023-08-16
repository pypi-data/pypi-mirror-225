import asyncio

import pyperclip
from bitcoin.signmessage import BitcoinMessage, SignMessage
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Center, Container, Horizontal
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Static


# class Notification(Static):
#     def on_mount(self) -> None:
#         self.set_timer(3, self.remove)

#     def on_click(self) -> None:
#         self.remove()


class CopyLabel(Label):
    def action_copy_clipboard(self, text: str):
        try:
            self.app.config.copy_callback(text)
        except Exception:  # Fix
            self.notify("No clipboard available", severity="warning")
        else:
            self.notify("Copied")

    # class Copied(Message):
    #     ...


class SignMessageOverlay(Screen):
    DEFAULT_CSS = """

    """

    BINDINGS = [
        ("ctrl+t", "app.toggle_dark", "Toggle Dark mode"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit"),
        (
            "escape",
            "app.pop_screen()",
            "home",
        ),
    ]

    def __init__(self, private_key: bytes) -> None:
        self.key = CBitcoinSecret.from_secret_bytes(private_key)
        self.address = P2PKHBitcoinAddress.from_pubkey(self.key.pub)

        super().__init__()

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Container(Button("X", variant="error", id="exit"), id="button_container"),
            Center(Static("SIGN MESSAGE"), id="title"),
            id="sign_top_bar",
        )

        yield Input("", placeholder="Enter Message", id="sign_message_input")
        yield Center(
            CopyLabel(
                f"Address: [@click=copy_clipboard('{self.address}')]{self.address}[/]"
            ),
            id="sign_message_address",
        )
        yield Horizontal(
            Button("Clear", variant="warning", id="sign_message_clear"),
            Button("Sign", variant="success", id="sign_message_submit"),
            id="sign_buttons",
        )

    def on_mount(self) -> None:
        message = self.query_one("Input", Input)
        self.set_focus(message)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        message = self.query_one("Input", Input)
        if event.button.id == "sign_message_submit" and message.value:
            sig_value = self.sign_message(message.value)
            sig = self.query("#sign_message_sig")
            if not sig:
                self.mount(
                    Center(
                        CopyLabel(
                            f"Signature: [@click=copy_clipboard('{sig_value}')]{sig_value}[/]"
                        ),
                        id="sign_message_sig",
                    )
                )

        if event.button.id == "sign_message_clear":
            message.value = ""
            sigs = self.query("#sign_message_sig")
            if sigs:
                sigs.last().remove()

            self.set_focus(message)

        if event.button.id == "exit":
            self.dismiss()

    def sign_message(self, msg: str) -> str:
        message = BitcoinMessage(msg)

        return SignMessage(self.key, message).decode()

    # def on_copy_label_copied(self):
    #     self.mount(Notification(Text("Copied!")))


if __name__ == "__main__":

    class BlahApp(App):
        def on_mount(self):
            self.push_screen(SignMessageOverlay())

    blah = BlahApp(css_path="/Users/davew/code/flux/wallet_app/app.css")
    blah.run()
