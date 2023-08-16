import datetime
import random
import secrets
import string

from rich.text import Text


def random_date() -> str:
    start_date = datetime.date(2022, 6, 1)
    end_date = datetime.date(2023, 6, 1)

    num_days = (end_date - start_date).days
    rand_days = random.randint(1, num_days)
    random_date = start_date + datetime.timedelta(days=rand_days)
    return str(random_date)


def random_dir() -> Text:
    if random.randint(0, 1):
        return Text("-->", style="bold green", justify="right")
    else:
        return Text("<--", style="bold red", justify="left")


def random_address() -> str:
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return f"t1{''.join(secrets.choice(alphabet) for i in range(33))}"


def random_txid() -> str:
    alphabet = string.ascii_lowercase + string.digits
    return "".join(secrets.choice(alphabet) for i in range(64))


def random_amount() -> float:
    places = random.randint(0, 5)
    return round(random.uniform(0.0, 1000.0), places)


ROWS = []
for n in range(50):
    ROWS.append(
        (random_txid(), random_date(), random_dir(), random_address(), random_amount())
    )
