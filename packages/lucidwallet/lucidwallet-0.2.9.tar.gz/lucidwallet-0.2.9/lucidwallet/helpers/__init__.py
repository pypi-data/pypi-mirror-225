from dataclasses import dataclass, field

from fluxwallet.db_new import Db, DbConfig, DbWallet
from fluxwallet.wallet import Wallet
from sqlalchemy import select
from textual.widgets import Static

import asyncio

from collections.abc import Callable

import keyring
from keyring.errors import NoKeyringError
import secrets
import pyperclip

import base64
import httpx


@dataclass
class NetworkData:
    price: float
    marketcap: int
    delta_24hr: float
    hashrate: int
    blockheight: int


@dataclass
class InitAppResponse:
    last_used_wallet: Wallet | None = None
    wallets: list[str] = field(default_factory=list)
    encrypted_db: bool = False
    networks: list[str] = field(default_factory=list)
    keyring_available: bool = False
    copy_callback: Callable | None = None
    show_market_data: bool = True
    network_data: NetworkData | None = None


async def get_db_info() -> tuple[Wallet | None, list[str], bool]:
    db = await Db.start()

    async with db as session:
        last_used_wallet: Wallet | None = None
        res = await session.scalars(select(DbWallet).order_by(DbWallet.id))
        wallets = res.all()

        if wallets:
            res = await session.scalars(
                select(DbConfig.value).filter_by(variable="last_used_wallet")
            )
            last_used_wallet_name = res.first()

            if not last_used_wallet_name:
                last_used_wallet_name = wallets[0].name
                await session.merge(
                    DbConfig(variable="last_used_wallet", value=last_used_wallet_name)
                )
                await session.commit()

            if last_used_wallet_name:
                last_used_wallet = await Wallet.open(last_used_wallet_name)

            wallets = [x.name for x in wallets]

            res = await session.scalars(
                select(DbConfig.value).filter_by(variable="show_market_data")
            )
            show_market_data = res.first()

            # if not set, we default to True
            if show_market_data is None:
                show_market_data = True
            else:
                show_market_data = bool(int(show_market_data))

        else:
            wallets = []
            show_market_data = True

    return last_used_wallet, wallets, db.encrypted, show_market_data


def write_tty(data: bytes) -> None:
    with open("/dev/tty", "wb") as f:
        f.write(data)
        f.flush()


def osc52_copy(data: str) -> None:
    data = bytes(data, encoding="utf-8")
    encoded = base64.b64encode(data)
    buffer = b"\033]52;p;" + encoded + b"\a"

    write_tty(buffer)


async def get_network_data() -> NetworkData:
    async with httpx.AsyncClient() as client:
        tasks = []
        tasks.append(
            client.get("https://api.coinpaprika.com/v1/tickers/zel-zelcash?quotes=USD")
        )

        tasks.append(
            client.get(
                "https://explorer.runonflux.io/api/status",
                params={"q": "getMiningInfo"},
            )
        )
        tasks.append(client.get("https://explorer.runonflux.io/api/sync"))
        market_data, mining_data, sync_info = await asyncio.gather(*tasks)
        market_data = market_data.json()
        mining_data = mining_data.json()
        sync_info = sync_info.json()

        price = market_data["quotes"]["USD"]["price"]
        marketcap = market_data["quotes"]["USD"]["market_cap"]
        delta_24hr = market_data["quotes"]["USD"]["percent_change_24h"]
        hashrate = mining_data["miningInfo"]["networkhashps"]
        blockheight = sync_info["height"]

        return NetworkData(price, marketcap, delta_24hr, hashrate, blockheight)


async def init_app() -> InitAppResponse:
    network_task = asyncio.create_task(get_network_data())

    (
        last_used_wallet,
        known_wallets,
        db_encrypted,
        show_market_data,
    ) = await get_db_info()

    random_user = secrets.token_hex(8)

    keyring_available = True
    try:
        # can use empty strings but seems dodgey
        keyring.get_password(random_user, random_user)
    except NoKeyringError:
        keyring_available = False

    try:
        # this will remove any copied stuff though
        pyperclip.copy("")
    except pyperclip.PyperclipException:
        copy_callback = osc52_copy
    else:
        copy_callback = pyperclip.copy

    wallet_networks = []
    if last_used_wallet:
        # this coudl error
        keys = await last_used_wallet.keys_networks()
        wallet_networks = [x.network.name for x in keys]

    network_data = await network_task

    return InitAppResponse(
        last_used_wallet,
        known_wallets,
        db_encrypted,
        wallet_networks,
        keyring_available,
        copy_callback,
        show_market_data,
        network_data,
    )
