#
#
from __future__ import annotations
from textual.app import App
from textual.widget import Widget
from textual.widgets import Static
from rich.segment import Segment
from textual.strip import Strip
from textual.geometry import Size
from rich.style import Style
from textual.containers import Container, Horizontal
from rich.color import Color
import hashlib
import importlib_metadata
from packaging import version

import httpx
from textual import work

from PIL import Image
import numpy as np
from pathlib import Path
from numpy.typing import NDArray

from textual.screen import Screen

### OTHER STUFF

import keyring

from lucidwallet.helpers import init_app
from lucidwallet.screens import (
    EncryptionPassword,
    WalletLanding,
)


package = "lucidwallet"


class Renderer:
    @classmethod
    def from_image(cls, path: Path) -> Renderer:
        img = np.asarray(Image.open(path))

        if len(img.shape) == 3:
            if img.shape[2] > 3:
                arr = np.array([[pixel[:3] for pixel in row] for row in img])
        elif len(img.shape) == 2:
            arr = np.array([[[pixel] * 3 for pixel in row] for row in img])

        return Renderer(arr)

    def __init__(self, img: NDArray) -> None:
        self.pixels = img

    @staticmethod
    def get_pixel(col: tuple[float, float, float]) -> Segment:
        color = Color.from_rgb(col[0], col[1], col[2])
        style = Style(bgcolor=color)
        return Segment("  ", style)

    def render_image(self, scale: tuple[float, float]) -> list[list[Segment]]:
        # first of all scale the image to the scale 'tuple'
        image_size = self.pixels.shape[:2]
        block_size = (image_size[0] / scale[0], image_size[1] / scale[1])
        blocks = []
        y = 0

        while y < image_size[0]:
            x = 0
            block_col = []
            while x < image_size[1]:
                # get a block, reshape in into an Nx3 matrix and then get average of each column
                block_col.append(
                    self.pixels[
                        int(y) : int(y + block_size[0]), int(x) : int(x + block_size[1])
                    ]
                    .reshape(-1, 3)
                    .mean(axis=0)
                )
                x += block_size[1]
            blocks.append(block_col)
            y += block_size[0]
        output = [[self.get_pixel(block) for block in row] for row in blocks]
        return output


class TextualImage(Widget):
    DEFAULT_CSS = """
    TextualImage {
        min-width: 60;
        min-height: 30;
        width: auto;
        height: auto;
        opacity: 0%;
    }
    """

    def __init__(self, image_path: Path) -> None:
        self.renderer = Renderer.from_image(image_path)
        self.output: list[list[Segment]] | None = None
        super().__init__()

    def on_mount(self):
        self.styles.animate("opacity", value=100.0, duration=3.0)

    def on_resize(self, new_size):
        self.generate_output()
        self.refresh()

    def generate_output(self) -> None:
        if self.size.width == self.app.size.width:
            max_size = min(self.app.size.width / 2, self.app.size.height)
            max_size = max_size * 0.8
        else:
            max_size = min(self.size.width / 2, self.size.height)

        self.output = self.renderer.render_image(scale=(max_size, max_size))

    def render_line(self, y: int) -> Strip:
        if not self.output:
            self.generate_output()

        if y + 1 > len(self.output):
            return Strip.blank(self.size.width, self.rich_style)

        row = self.output[y]

        strip = Strip(row)
        return strip


class LoadingScreen(Screen):
    DEFAULT_CSS = """
    LoadingScreen {
        width: 100%;
        height: 1fr;
        align: center middle;
        background: black;
        border: tall $primary;
    }
    LoadingScreen Static {
        border: greenyellow;
        width: auto;
    }
    """

    # def on_show(self):
    #     self.set_timer(3, self.dismiss)

    def compose(self):
        yield Static("Lucidwallet")
        yield TextualImage(Path("static/images/flux_img.png"))

    @work(name="version_check")
    async def version_check(self) -> None:
        if new_version := await self.new_version_available():
            self.call_after_refresh(
                self.notify, f"New version {new_version} available", timeout=5
            )

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

    async def valid_password(self) -> bool:
        return await self.config.last_used_wallet.db.validate_key()

    async def encryption_password_callback(self, result: tuple[str, bool]) -> None:
        password, store_in_keychain = result

        hashed = hashlib.sha256(bytes(password, "utf8")).hexdigest()
        self.config.last_used_wallet.db.set_encrypted_key(hashed)

        if not await self.valid_password():
            self.app.switch_screen(
                EncryptionPassword(message="Invalid Password"),
                self.encryption_password_callback,
            )
            return

        if store_in_keychain:
            keyring.set_password("fluxwallet", "fluxwallet_user", hashed)

        self.app.install_screen(
            WalletLanding(
                self.config.last_used_wallet, self.config.networks, self.config.wallets
            ),
            name="wallet_landing",
        )
        self.app.switch_screen("wallet_landing")

    @work(group="boot")
    async def boot(self) -> None:
        self.app.config = await init_app()

        if not self.app.config.last_used_wallet:
            self.app.switch_screen("welcome")
            return

        if self.app.config.encrypted_db:
            password_hash = ""

            if self.app.config.keyring_available:
                password_hash = keyring.get_password("fluxwallet", "fluxwallet_user")

            if not password_hash:
                self.app.switch_screen(
                    EncryptionPassword(), self.encryption_password_callback
                )
                return
            else:
                # this only ever needs to get set once
                self.app.config.last_used_wallet.db.set_encrypted_key(password_hash)

                if not await self.valid_password():
                    if self.app.config.keyring_available:
                        keyring.delete_password("fluxwallet", "fluxwallet_user")

                    self.app.switch_screen(
                        EncryptionPassword(message="Invalid Password"),
                        self.encryption_password_callback,
                    )
                    return

        self.app.install_screen(
            WalletLanding(
                self.app.config.last_used_wallet,
                self.app.config.networks,
                self.app.config.wallets,
            ),
            name="wallet_landing",
        )
        self.app.switch_screen("wallet_landing")

    async def on_show(self) -> None:
        self.call_after_refresh(self.boot)


# class BlahApp(App):
#     def on_mount(self):
#         self.push_screen(LoadingScreen())


# app = BlahApp()
# app.run()
