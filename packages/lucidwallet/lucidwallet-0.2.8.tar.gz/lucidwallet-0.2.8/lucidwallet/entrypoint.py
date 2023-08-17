import hashlib
import os

import keyring
from packaging import version

from textual import on, work
from textual.app import App
from textual.binding import Binding

import asyncio
from lucidwallet.helpers import init_app
from lucidwallet.screens import (
    LoadingScreen,
    CreateWallet,
    EncryptionPassword,
    FirstRun,
    ImportFromMnemonic,
    MnemonicOverlay,
    WalletLanding,
)


import platform

import httpx
import importlib_metadata


package = "lucidwallet"


class LucidWallet(App[None]):
    CSS_PATH = "app.css"
    SCREENS = {
        "welcome": FirstRun(),
        "create_wallet": CreateWallet(),
        "from_mnemonic": ImportFromMnemonic(),
        "loading": LoadingScreen(),
    }
    BINDINGS = [
        ("ctrl+t", "app.toggle_dark", "Toggle Dark mode"),
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True),
    ]

    async def new_version_available(self) -> str | None:
        current_version = importlib_metadata.version(package)
        current_version = version.parse(current_version)
        # shame we have to download the entire package info for just the version
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"https://pypi.org/pypi/{package}/json")
        except httpx.HTTPError:
            return

        try:
            latest_version = response.json()["info"]["version"]
        except KeyError:
            return

        latest_version = version.parse(latest_version)

        return latest_version if latest_version > current_version else None

    @work(name="version_check")
    async def version_check(self) -> None:
        if new_version := await self.new_version_available():
            self.call_after_refresh(
                self.notify, f"New version {new_version} available", timeout=5
            )

    async def valid_password(self) -> bool:
        return await self.config.last_used_wallet.db.validate_key()

    async def encryption_password_callback(self, result: tuple[str, bool]) -> None:
        password, store_in_keychain = result

        hashed = hashlib.sha256(bytes(password, "utf8")).hexdigest()
        self.config.last_used_wallet.db.set_encrypted_key(hashed)

        if not await self.valid_password():
            self.push_screen(
                EncryptionPassword(message="Invalid Password"),
                self.encryption_password_callback,
            )
            return

        if store_in_keychain:
            keyring.set_password("fluxwallet", "fluxwallet_user", hashed)

        self.install_screen(
            WalletLanding(
                self.config.last_used_wallet, self.config.networks, self.config.wallets
            ),
            name="wallet_landing",
        )
        self.push_screen("wallet_landing")

    async def boot(self) -> None:
        self.version_check()

        self.config = await init_app()

        if not self.config.last_used_wallet:
            self.push_screen("welcome")
            return

        if self.config.encrypted_db:
            password_hash = ""

            if self.config.keyring_available:
                password_hash = keyring.get_password("fluxwallet", "fluxwallet_user")

            if not password_hash:
                self.push_screen(
                    EncryptionPassword(), self.encryption_password_callback
                )
                return
            else:
                # this only ever needs to get set once
                self.config.last_used_wallet.db.set_encrypted_key(password_hash)

                if not await self.valid_password():
                    if self.config.keyring_available:
                        keyring.delete_password("fluxwallet", "fluxwallet_user")

                    self.push_screen(
                        EncryptionPassword(message="Invalid Password"),
                        self.encryption_password_callback,
                    )
                    return

        self.install_screen(
            WalletLanding(
                self.config.last_used_wallet, self.config.networks, self.config.wallets
            ),
            name="wallet_landing",
        )
        self.push_screen("wallet_landing")

    # async def on_load(self) -> None:
    #     self.push_screen("loading")

    async def on_mount(self) -> None:
        # await self.boot()
        # push loading screen first, with logo
        self.push_screen("loading")

    # fix these
    @on(MnemonicOverlay.WalletCreated)
    async def on_mnemonic_overlay_wallet_created(
        self, event: MnemonicOverlay.WalletCreated
    ):
        wallet_landing: WalletLanding = self.get_screen("wallet_landing")
        await wallet_landing.new_wallet_created(event.wallet)

    @on(ImportFromMnemonic.WalletCreated)
    async def on_import_from_mnemonic_wallet_created(
        self, event: ImportFromMnemonic.WalletCreated
    ):
        wallet_landing: WalletLanding = self.get_screen("wallet_landing")
        await wallet_landing.new_wallet_created(event.wallet)


# for console script
def run():
    # ubuntu by default doesn't have truecolor set, so the colors are weird
    os.environ["COLORTERM"] = "truecolor"
    # just in case it's been modified
    os.environ["TERM"] = "xterm-256color"

    if platform.system() == "Windows":
        from importlib_resources import files

        dll_path = files("lucidwallet.ssl_win")
        with os.add_dll_directory(dll_path):
            app = LucidWallet()
            app.run()


# for textual console
if __name__ == "__main__":
    run()
