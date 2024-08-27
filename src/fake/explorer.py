from models.explorer import Explorer
from errors import Missing, Duplicate

fakes: list[Explorer] = [
    Explorer(name="snurfle", country="ru", description="some thing"),
    Explorer(name="scoot", country="us", description="some other thing"),
    Explorer(name="fsf", country="da", description="some other thing"),
]


def find(name: str) -> Explorer | None:
    for explorer in fakes:
        if explorer.name == name:
            return explorer
    return None


def check_missing(name: str) -> None:
    if not find(name):
        raise Missing(msg=f"Explorer {name} not found")


def check_duplicate(name: str) -> None:
    if find(name):
        raise Duplicate(msg=f"Explorer {name} already exists")


def get_all() -> list[Explorer]:
    return fakes


def get_one(name: str) -> Explorer | None:
    check_missing(name)
    return find(name)


def create(explorer: Explorer) -> Explorer:
    check_duplicate(explorer.name)
    fakes.append(explorer)
    return explorer


def modify(name: str, explorer: Explorer) -> Explorer:
    check_missing(name)
    for i in range(len(fakes)):
        if fakes[i].name == name:
            fakes[i] = explorer
    return explorer


def delete(name: str) -> None:
    check_missing(name)
    fakes.remove(find(name))
    return None
