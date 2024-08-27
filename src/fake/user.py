from models.user import User
from errors import Missing, Duplicate

fakes = [
    User(name="user1", hash="hash1"),
    User(name="user2", hash="hash2"),
    User(name="user3", hash="hash3"),
]


def find(name: str) -> User | None:
    for user in fakes:
        if user.name == name:
            return user
    return None


def check_missing(name: str) -> None:
    if not find(name):
        raise Missing(msg=f"User {name} not found")


def check_duplicate(name: str) -> None:
    if find(name):
        raise Duplicate(msg=f"User {name} already exists")


def get_all() -> list[User]:
    return fakes


def get_one(name: str) -> User | None:
    check_missing(name)
    return find(name)


def create(user: User) -> User:
    check_duplicate(user.name)
    fakes.append(user)
    return user


def modify(name: str, user: User) -> User:
    check_missing(name)
    for i in range(len(fakes)):
        if fakes[i].name == name:
            fakes[i] = user
    return user


def delete(name: str) -> None:
    check_missing(name)
    fakes.remove(find(name))
    return None
