import os
import pytest
from models.creature import Creature
from errors import Missing, Duplicate

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import creature


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="Yeti",
        area="Himalayas",
        country="CN",
        description="Hristute Himalayan",
        aka="Abominable Snowman",
    )


def test_create(sample: Creature):
    resp = creature.create(sample)
    assert resp == sample


def test_get_all(sample: Creature):
    resp = creature.get_all()
    assert resp == [sample]


def test_create_duplicate(sample: Creature):
    with pytest.raises(Duplicate):
        creature.create(sample)


def test_get_one(sample: Creature):
    resp = creature.get_one(sample.name)
    assert resp == sample


def test_get_one_missing(sample: Creature):
    with pytest.raises(Missing):
        creature.get_one("404")


def test_modify(sample: Creature):
    sample.area = "Sesame Street"
    resp = creature.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing():
    thing: Creature = Creature(
        name="snurfle", country="ru", area="", description="some thing", aka=""
    )
    with pytest.raises(Missing):
        creature.modify(thing.name, thing)


def test_delete(sample: Creature):
    resp = creature.delete(sample.name)
    assert resp is None


def test_delete_missing(sample: Creature):
    with pytest.raises(Missing):
        creature.delete(sample.name)
