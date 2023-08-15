import asyncio
import time
from collections.abc import Awaitable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from fluxwallet.db_new import DbKey
from fluxwallet.values import Value
from fluxwallet.wallet import Wallet, WalletTransaction
from rich.text import Text

from lucidwallet.events import Event


class ScanType(Enum):
    PERIODIC = "PERIODIC"
    NEW_KEY = "NEW_KEY"
    FULL_WALLET = "FULL_WALLET"


@dataclass
class Timer:
    callback: Awaitable
    interval: int = 10
    run_on_start: bool = True
    loop_task: asyncio.Task | None = None

    def start(self) -> None:
        if not self.loop_task or self.loop_task.cancelled():
            self.loop_task = asyncio.create_task(self.loop())

    async def reset(self, run_on_start: bool = True) -> None:
        self.run_on_start = run_on_start

        await self.stop()
        self.start()

    async def stop(self) -> None:
        if not self.loop_task:
            return

        self.loop_task.cancel()

        try:
            await self.loop_task
        except asyncio.CancelledError:
            pass

    async def loop(self) -> None:
        if self.run_on_start:
            await self.callback()

        while True:
            await asyncio.sleep(self.interval)
            await self.callback()


@dataclass
class Network:
    offset: int = 0
    transactions: list[WalletTransaction] = field(default_factory=list)
    table_rows: list[tuple] = field(default_factory=list)
    last_scanned_periodic: float = 0.0
    last_scanned_full: float = 0.0
    scroll_height: float = 0.0
    scanning: bool = False
    first_scan: bool = True
    balance: float = 0.0  # cache value for when scanning

    def reset(self) -> None:
        """Default network back to starting values"""
        self.offset = 0
        self.last_scanned = 0.0
        self.scanning = False
        self.transactions = []
        self.table_rows = []
        self.scroll_height = 0.0
        self.first_scan = True


@dataclass
class WalletData:
    wallet: Wallet
    networks: dict[str, Network] = field(default_factory=dict)

    def reset_networks(self) -> None:
        """Reset all networks back to default values"""
        for network in self.networks.values():
            network.reset()


@dataclass
class FluxWalletDataStore:
    current_wallet: str | None = None
    current_network: str = "flux"
    wallet_names: set[str] = field(default_factory=set)
    wallets: dict[str, WalletData] = field(default_factory=dict)
    unconfirmed_txs: list[WalletTransaction] = field(default_factory=list)
    scan_timer: Timer | None = None
    tx_history_scanning: bool = False

    def get_current_wallet(self) -> Wallet:
        return self.wallets[self.current_wallet].wallet

    def get_current_wallet_networks(self) -> list[str]:
        return self.wallets[self.current_wallet].networks

    def get_transaction(self, txid: str) -> WalletTransaction | None:
        wallet_data = self.wallets[self.current_wallet]

        tx = next(
            filter(
                lambda x: x.tx.txid == txid,
                wallet_data.networks[self.current_network].transactions,
            ),
            None,
        )

        return tx

    def add_timer(self, timer: Timer):
        self.scan_timer = timer

    def exists(self, wallet: str | Wallet) -> bool:
        if isinstance(wallet, Wallet):
            wallet = wallet.name

        return True if wallet in self.wallets else False

    async def store_wallet(self, wallet: str | Wallet) -> None:
        if isinstance(wallet, str):
            wallet = await Wallet.open(wallet)

        keys = await wallet.keys_networks()
        networks = {x.network.name: Network() for x in keys}
        self.wallets[wallet.name] = WalletData(wallet, networks)

    async def receive_address(self, wallet_name: str, network: str) -> str:
        next_unused_key = await self.wallets[wallet_name].wallet.get_key(
            network=network
        )
        return next_unused_key.address

    def get_last_network_balance(self, wallet_name: str, network_name: str) -> float:
        return self.wallets[wallet_name].networks[network_name].balance

    def set_last_network_balance(
        self, wallet_name: str, network_name: str, balance: float
    ) -> float:
        self.wallets[wallet_name].networks[network_name].balance = balance

    async def balance(self, wallet_name: str, network: str) -> float:
        if self.is_network_scanning(wallet_name, network):
            balance = self.get_last_network_balance(wallet_name, network)
        else:
            balance = await self.wallets[wallet_name].wallet.balance(network=network)
            self.set_last_network_balance(wallet_name, network, balance)

        return balance

    async def current_network_balance(self) -> float:
        return await self.balance(self.current_wallet, self.current_network)

    async def set_current_wallet(self, wallet: str | Wallet) -> None:
        if not self.exists(wallet):
            await self.store_wallet(wallet)

        self.current_wallet = str(wallet)

        # change this to default or something
        self.set_current_network("flux")

    def set_current_network(self, network_name: str) -> None:
        self.current_network = network_name

    def get_current_network(self) -> str:
        return self.current_network

    async def get_current_wallet_spend_info(self) -> tuple[str, float]:
        receive_address = await self.receive_address(
            self.current_wallet, self.current_network
        )

        balance = await self.balance(self.current_wallet, self.current_network)

        return (receive_address, balance)

    async def parse_wallet_txs(
        self, wallet_name: str, wallet_txs: list[WalletTransaction]
    ) -> tuple:
        TX_DIRECTION = {
            False: Text("-->", style="bold green", justify="right"),
            True: Text("<--", style="bold red", justify="left"),
        }

        parsed_txs = []

        used_keys: list[DbKey] = await self.wallets[wallet_name].wallet.keys(
            used=True, network=self.current_network
        )
        used_addresses = [x.address for x in used_keys]

        for wt in wallet_txs:
            if wt.tx.date:
                date = wt.tx.date
                date = date.replace(tzinfo=timezone.utc)
                # local
                date = date.astimezone()
            else:
                date = datetime.now()

            outbound = False
            for input in wt.tx.inputs:
                if input.address in used_addresses:
                    outbound = True
                    break

            value = 0
            for output in wt.tx.outputs:
                if outbound:
                    if not output.address in used_addresses:
                        # this is who the output is to
                        value += output.value
                else:
                    if output.address in used_addresses:
                        value += output.value

            value = Value.from_satoshi(value, network=self.current_network).str(
                1, currency_repr=None
            )
            parsed_txs.append(
                (
                    wt.tx.txid,
                    TX_DIRECTION[outbound],
                    date.date(),
                    date.strftime("%H:%M:%S"),
                    value,
                    self.current_network.upper(),
                )
            )

        return parsed_txs

    async def get_txs(
        self,
        response: asyncio.Queue,
        wallet_name: str,
        network: str,
        latest_only: bool = False,
        limit: int = 60,
    ) -> None:
        offset = (
            0 if latest_only else self.wallets[wallet_name].networks[network].offset
        )

        tx_gen = self.wallets[wallet_name].wallet.transactions_full(
            network=network, limit=limit, offset=offset
        )

        async for txs in tx_gen:
            self.wallets[wallet_name].networks[network].offset += len(txs)

            self.wallets[wallet_name].networks[network].transactions.extend(txs)

            if parsed_txs := await self.parse_wallet_txs(wallet_name, txs):
                self.wallets[wallet_name].networks[network].table_rows.extend(
                    parsed_txs
                )
                await response.put(Event(type=Event.EventType.NewRows, rows=parsed_txs))

    async def get_transactions_from_db(
        self,
        response: asyncio.Queue,
        force: bool = False,
        latest_only: bool = False,
        limit: int = 60,
    ) -> None:
        """_summary_

        Args:
            force (bool, optional): force db query for new txs. Defaults to False.
            latest_only (bool, optional): will force db query and only retrieve latest
            txs from db, ignoring internal offset. Defaults to False.
            limit (int, optional): how many txs to fetch. Defaults to 60.
        """
        if not force and self.current_network_has_table_rows():
            await response.put(
                Event(
                    type=Event.EventType.NewRows, rows=self.current_network_table_rows()
                )
            )
            await response.put(
                Event(
                    type=Event.EventType.Scroll,
                    scroll_height=self.get_current_network_scroll_height(),
                )
            )
            return

        await self.get_txs(
            response,
            self.current_wallet,
            self.current_network,
            latest_only,
            limit=limit,
        )

    def current_network_has_table_rows(self) -> bool:
        has_rows = bool(len(self.current_network_table_rows()))
        return has_rows

    def current_network_table_rows(self) -> list[tuple]:
        return (
            self.wallets[self.current_wallet].networks[self.current_network].table_rows
        )

    def store_current_network_scroll_height(self, scroll_height: int) -> None:
        self.wallets[self.current_wallet].networks[
            self.current_network
        ].scroll_height = scroll_height

    def get_current_network_scroll_height(self) -> int:
        return (
            self.wallets[self.current_wallet]
            .networks[self.current_network]
            .scroll_height
        )

    def reset_current_wallet_datastore(self) -> None:
        self.wallets[self.current_wallet].reset_networks()

    def set_scanning_for_network(self, wallet_name: str, network_name: str) -> None:
        self.wallets[wallet_name].networks[network_name].scanning = True

    def unset_scanning_for_network(self, wallet_name: str, network_name: str) -> None:
        self.wallets[wallet_name].networks[network_name].scanning = False

    def is_network_scanning(self, wallet_name: str, network_name: str) -> bool:
        return self.wallets[wallet_name].networks[network_name].scanning

    def is_current_network_scanning(self) -> bool:
        return self.is_network_scanning(self.current_wallet, self.current_network)

    def set_last_scanned_for_network(
        self, wallet: str, network: str, scan_type: ScanType
    ) -> None:
        if scan_type == ScanType.PERIODIC:
            self.wallets[wallet].networks[
                network
            ].last_scanned_periodic = time.monotonic()
        else:  # Full
            self.wallets[wallet].networks[network].last_scanned_full = time.monotonic()

    def scan_for_current_network_required(self, scan_type: ScanType) -> bool:
        scan_required = True
        now = time.monotonic()

        recent_periodic = (
            self.get_current_network_last_scan_time(ScanType.PERIODIC) + 15 > now
        )
        recent_full = (
            self.get_current_network_last_scan_time(ScanType.FULL_WALLET) + 15 > now
        )

        if scan_type == ScanType.FULL_WALLET:
            if recent_full:
                scan_required = False

        if scan_type == ScanType.PERIODIC:
            if recent_periodic or recent_full:
                scan_required = False

        return scan_required

    def get_current_network_last_scan_time(self, scan_type: ScanType) -> float:
        # fix all this
        if scan_type == ScanType.PERIODIC:
            return (
                self.wallets[self.current_wallet]
                .networks[self.current_network]
                .last_scanned_periodic
            )
        else:  # full
            return (
                self.wallets[self.current_wallet]
                .networks[self.current_network]
                .last_scanned_full
            )

    def is_network_first_scan(self, wallet_name: str, network_name: str) -> bool:
        return self.wallets[wallet_name].networks[network_name].first_scan

    def set_network_scanned(self, wallet_name: str, network_name: str) -> None:
        self.wallets[wallet_name].networks[network_name].first_scan = False

    def add_known_wallet(self, wallet: str) -> None:
        self.wallet_names.add(wallet)

    def get_known_wallets(self) -> list:
        return list(self.wallet_names)

    def add_unconfirmed_tx(self, tx: WalletTransaction) -> None:
        self.unconfirmed_txs.append(tx)

    def start_scan_timer(self) -> None:
        if self.scan_timer:
            self.scan_timer.start()

    async def reset_timer(self, run_on_start: bool = True) -> None:
        await self.scan_timer.reset(run_on_start)
