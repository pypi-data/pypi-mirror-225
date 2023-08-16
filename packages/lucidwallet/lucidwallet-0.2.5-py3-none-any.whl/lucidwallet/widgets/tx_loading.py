from textual.app import ComposeResult
from textual.containers import Container
from textual.widget import Widget
from textual.widgets import LoadingIndicator, Static


class TxLoading(Widget):
    DEFAULT_CSS = """
    # TxLoading>Container {
    #     max-width: 16;
    #     height: 100%;
    #     opacity: 0%;
    #     align: left middle;
    #     margin-right: 2;
    # }
    # TxLoading > Vertical {
    #     max-height: 5;
    #     border: round $primary;
    # }
    # #scanning {
    #     margin-left: 2;
    #     width: auto;
    # }
    # #transactions {
    #     margin-left: 1;
    #     width: auto;
    # }
    # TxLoading LoadingIndicator {
    #     max-width: 15;
    #     max-height: 1;
    #     # height: auto;
    #     # width: auto;
    #     border: blank;
    # }
    """

    def compose(self) -> ComposeResult:
        yield Container(
            Static("Scanning", id="tx_loading_scanning"),
            LoadingIndicator(),
            Static("Transactions", id="tx_loading_transactions"),
        )
