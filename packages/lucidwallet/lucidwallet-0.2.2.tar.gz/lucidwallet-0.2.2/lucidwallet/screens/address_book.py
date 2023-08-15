from functools import partial
from typing import Iterable

from fluxwallet.db import Db, DbAddressBook
from rich.text import Text
from textual import on
from textual.app import App, ComposeResult
from textual.containers import Center, Horizontal
from textual.message import Message
from textual.reactive import var
from textual.screen import Screen
from textual.validation import Function, Regex
from textual.widgets import Button, DataTable, Input

from lucidwallet.screens import AddressBookOverlay


class AddressBook(Screen[str | None]):
    DEFAULT_CSS = """
    AddressBook {
        width: 1fr;
        align: center top;
        border: double $primary;
        padding: 2;
        margin: 4;
        border-title-align: center;
        border-title-color: $secondary;

    }
    AddressBook > Input {
        margin-bottom: 1;
    }

    AddressBook > Horizontal {
        margin: 1;
        height: auto;
        align: center top;
    }
        AddressBook > Horizontal > Button {
        margin: 1;
    }

    AddressBook>Center>DataTable {
        background: $primary-background;
        width: auto;
    }
    """

    address = var("")

    def __init__(self, address: str | None = None, return_nickname: bool = False):
        self._address = address

        self.return_nickname = return_nickname
        self.table = None

        super().__init__()

    def on_mount(self):
        self.border_title = "Address book"
        self.address = self._address

        self.table = self.query_one("DataTable", DataTable)

        for col in ["Nickname", "Address", "Remove"]:
            self.table.add_column(col)

        self.session = Db().session
        self.fetch_address_book()

        # table.cursor_type = "row"

    def on_unmount(self):
        self.session.close()

    def fetch_address_book(self):
        address_book: Iterable[DbAddressBook] = self.session.query(DbAddressBook).all()

        for row in address_book:
            print(
                "ROW",
                repr(
                    self.table.add_row(
                        row.name,
                        row.address,
                        Text("X", style="bold red", justify="center"),
                    )
                ),
            )

    def validate_address_input(self, address: str) -> bool:
        if address == "":
            return True

        if address.startswith(("t1", "t3")) and len(address) == 35:
            self.sendto_address = address
            return True
        return False

    def compose(self) -> ComposeResult:
        yield Input(
            None,
            validators=[Regex("^[a-zA-Z0-9_-]*$")],
            placeholder="Address nickname. Must only contain: a-z A-Z 0-9, underscore or hyphen",
            id="nickname",
        )
        yield Input(
            self._address,
            validators=[
                Function(function=self.validate_address_input),
            ],
            placeholder="Address",
            id="address",
        )
        yield Horizontal(
            Button("Save", id="address_save"),
            Button("Cancel", variant="error", id="cancel"),
        )
        yield Center(DataTable())

    @on(Input.Changed, "#address")
    def address_input_changed(self, event: Input.Changed) -> None:
        event.stop()

        if not event.validation_result.failures:
            self.addresxs = event.value
        else:
            self.address = ""

    @on(Button.Pressed)
    def on_button_pressed(self, event: Button.Pressed) -> None:
        event.stop()

        nickname = None

        if event.button.id == "address_save":
            nickname = self.query_one("#nickname", Input).value
            self.save_nickname(nickname, self.address)
            self.table.add_row(
                nickname, self.address, Text("X", justify="center", style="bold red")
            )
            # clear values

            if not self.return_nickname:
                nickname = None
        else:
            self.dismiss(nickname)

    def save_nickname(self, nickname: str, address: str):
        if not nickname:
            return

        address_book_entry: DbAddressBook = (
            self.session.query(DbAddressBook).filter_by(name=nickname).scalar()
        )

        if not address_book_entry:
            new_ab_entry = DbAddressBook(
                name=nickname,
                address=address,
            )
            self.session.add(new_ab_entry)
        else:
            address_book_entry.address = address

        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

    def on_input_submitted(self):
        self.focus_next()

    def watch_address(self, new_value: bool) -> None:
        button = self.query_one("#address_save", Button)

        if new_value:
            button.disabled = False
            button.variant = "success"
        else:
            button.disabled = True
            button.variant = "default"

    def on_delete_row_callback(self, table: DataTable, row_key, delete: bool) -> None:
        if delete:
            nickname, _, _ = table.get_row(row_key)
            table.remove_row(row_key)
            self.session.query(DbAddressBook).filter_by(name=nickname).delete()
            self.session.commit()

    def on_data_table_cell_selected(self, event: DataTable.CellSelected):
        if str(event.value) == "X":
            table = self.query_one("DataTable", DataTable)
            nickname, address, _ = table.get_row(event.cell_key.row_key)
            callback = partial(
                self.on_delete_row_callback, table, event.cell_key.row_key
            )
            self.app.push_screen(
                AddressBookOverlay(nickname, address), callback=callback
            )
