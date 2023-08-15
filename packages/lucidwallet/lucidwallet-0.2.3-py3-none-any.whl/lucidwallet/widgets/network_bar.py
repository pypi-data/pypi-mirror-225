from rich.text import Text
from textual.app import ComposeResult
from textual.reactive import var
from textual.widget import Widget
from textual.widgets import Button, Static

from textual import work
from textual.app import App
from rich.text import Text

from fluxwallet.db_new import Db, DbConfig

from decimal import Decimal

# to display

# Blockheight: 1446174 Hashrate: 1.8 MS/S Price 0.41 USD Marketcap: 130.1M USD 24Hr: ↑0.43%


class NetworkBar(Widget):
    DEFAULT_CSS = """
    # NetworkBar {
    #     margin-top: 1;
    #     layout: horizontal;
    #     background: $panel;
    #     height: 3;
    # }
    # NetworkBar>Static {
    #     content-align: center middle;
    #     border: tall $primary;
    #     width: 1fr;
    # }
    # NetworkBar>Button {
    #     dock: right;
    #     width: auto;
    #     min-width: 0;
    #     margin-right: 0;
    #     border: tall $primary;
    # }
    # NetworkBar>Button:focus {
    #     text-style: none;
    #     background: black 80%;
    # }
    """

    blockheight = var(0)
    hashrate = var(0.0)
    price = var(0.0)
    marketcap = var(0)
    delta_24hr = var(0.0)
    show_market_data = var(True)

    def __init__(
        self,
        blockheight: int = 0,
        hashrate: float = 0.0,
        price: float = 0.0,
        marketcap: float = 0.0,
        delta_24hr: float = 0.0,
        show_market_data: bool = True,
    ) -> None:
        self._blockheight = blockheight
        self._hashrate = hashrate
        self._price = price
        self._marketcap = marketcap
        self._delta_24hr = delta_24hr
        self._show_market_data = show_market_data

        self.db = Db()

        super().__init__()

    def on_mount(self) -> None:
        self.blockheight = self._blockheight
        self.hashrate = self._hashrate
        self.price = self._price
        self.marketcap = self._marketcap
        self.delta_24hr = self._delta_24hr
        self.show_market_data = self._show_market_data

    def compose(self) -> ComposeResult:
        yield Static(
            self.build_blockheight(), id="blockheight", classes="networkbar_item"
        )
        yield Static(self.build_hashrate(), id="hashrate", classes="networkbar_item")
        yield Button("\U0001F4B0", id="market_data_toggle")

        if self._show_market_data:
            yield Static(
                self.build_price(), id="price", classes="marketdata networkbar_item"
            )
            yield Static(
                self.build_marketcap(),
                id="marketcap",
                classes="marketdata networkbar_item",
            )
            yield Static(
                self.build_delta_24hr(),
                id="delta_24hr",
                classes="marketdata networkbar_item",
            )

    def build_blockheight(self) -> Text:
        return Text(f"Blockheight: {self._blockheight}")

    def build_hashrate(self) -> Text:
        return Text(f"Hashrate: {round(self._hashrate / 10**6, 2)} MS/s")

    def build_price(self) -> Text:
        # decimal will print the 3rd digit if its 0
        return Text(f"Price: {round(Decimal(self._price), 3)} USD")

    def build_marketcap(self) -> Text:
        return Text(f"Marketcap: {round(self._marketcap / 10**6, 2)}M USD")

    def build_delta_24hr(self) -> Text:
        UP_ARROW = "\U00002191"
        DOWN_ARROW = "\U00002193"
        positive_style = "bold green"
        negative_style = "bold red"

        if self._delta_24hr >= 0:
            symbol = UP_ARROW
            style = positive_style
        else:
            symbol = DOWN_ARROW
            style = negative_style

        delta = Text.assemble("24hr: ", (f"{symbol} {self._delta_24hr} %", style))

        return delta

    @work(group="set_db_show_market_data", exclusive=True)
    async def set_db_show_market_data(self, show_market_data: bool) -> None:
        async with self.db.get_session() as session:
            await session.merge(
                DbConfig(variable="show_market_data", value=str(int(show_market_data)))
            )
            await session.commit()

    def watch_blockheight(self, new_value: int) -> None:
        self._blockheight = new_value

        height = self.query_one("#blockheight", Static)
        height.update(self.build_blockheight())

    def watch_hashrate(self, new_value: float) -> None:
        self._hashrate = new_value

        hashrate = self.query_one("#hashrate", Static)
        hashrate.update(self.build_hashrate())

    def watch_price(self, new_value: float) -> None:
        self._price = new_value

        if self._show_market_data:
            price = self.query_one("#price", Static)
            price.update(self.build_price())

    def watch_marketcap(self, new_value: float) -> None:
        self._marketcap = new_value

        if self._show_market_data:
            marketcap = self.query_one("#marketcap", Static)
            marketcap.update(self.build_marketcap())

    def watch_delta_24hr(self, new_value: float) -> None:
        self._delta_24hr = new_value

        if self._show_market_data:
            delta_24hr = self.query_one("#delta_24hr", Static)
            delta_24hr.update(self.build_delta_24hr())

    def watch_show_market_data(self, new_value: bool) -> None:
        if self._show_market_data == new_value:
            return

        if not self._show_market_data and new_value:
            self.mount(
                Static(
                    self.build_price(), id="price", classes="marketdata networkbar_item"
                )
            )
            self.mount(
                Static(
                    self.build_marketcap(),
                    id="marketcap",
                    classes="marketdata networkbar_item",
                )
            )
            self.mount(
                Static(
                    self.build_delta_24hr(),
                    id="delta_24hr",
                    classes="marketdata networkbar_item",
                )
            )
        else:
            market_data = self.query(".marketdata")
            for widget in market_data:
                widget.remove()

        self.set_db_show_market_data(new_value)

        self._show_market_data = new_value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.show_market_data = False if self.show_market_data == True else True


if __name__ == "__main__":

    class blahApp(App):
        def compose(self):
            self.bar = NetworkBar()
            yield self.bar

        def on_mount(self):
            self.bar.blockheight = 1446174
            self.bar.hashrate = 1801598
            self.bar.price = 0.41
            self.bar.marketcap = 129989111
            self.bar.delta_24hr = 0.47
            self.call_after_refresh(self.set_focus, None)

    app = blahApp()
    app.run()
