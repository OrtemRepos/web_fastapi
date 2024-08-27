import os
from models.creature import Creature
from errors import Missing, Duplicate
from service import creature as code
import pytest

os.environ["CRYPTID_UNIT_TEST"] = "true"


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
    resp = code.create(sample)
    assert resp == sample


def test_create_duplicate(sample: Creature):
    with pytest.raises(Duplicate):
        code.create(sample)


def test_get_exists(sample: Creature):
    resp = code.get_one(sample.name)
    assert resp == sample


def test_get_not_exists(sample: Creature):
    with pytest.raises(Missing):
        code.get_one("Snowman")


def test_modify(sample: Creature):
    sample.aka = "Snowman"
    resp = code.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing(sample: Creature):
    with pytest.raises(Missing):
        code.modify("Snowman", sample)


def test_delete(sample: Creature):
    resp = code.delete(sample.name)
    assert resp is None


def test_delete_missing(sample: Creature):
    with pytest.raises(Missing):
        code.delete("Snowman")
