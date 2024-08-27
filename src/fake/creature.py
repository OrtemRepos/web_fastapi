from models.creature import Creature
from errors import Missing, Duplicate

fakes = [
    Creature(
        name="Yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hristute Himalayan",
    ),
    Creature(
        name="Bigfoot",
        description="Bigfoot, or bigfoot is a giant earthworm native to the Americas.",
        country="US",
        area="*",
        aka="Sasquatch",
    ),
]


def find(name: str) -> Creature | None:
    for creature in fakes:
        if creature.name == name:
            return creature
    return None


def check_missing(name: str) -> None:
    if not find(name):
        raise Missing(msg=f"Creature {name} not found")


def check_duplicate(name: str) -> None:
    if find(name):
        raise Duplicate(msg=f"Creature {name} already exists")


def get_all() -> list[Creature]:
    return fakes


def get_one(name: str) -> Creature | None:
    check_missing(name)
    return find(name)


def create(creature: Creature) -> Creature:
    check_duplicate(creature.name)
    fakes.append(creature)
    return creature


def modify(name: str, creature: Creature) -> Creature:
    check_missing(name)
    for i in range(len(fakes)):
        if fakes[i].name == name:
            fakes[i] = creature
    return creature


def delete(name: str) -> None:
    check_missing(name)
    fakes.remove(find(name))
    return None
