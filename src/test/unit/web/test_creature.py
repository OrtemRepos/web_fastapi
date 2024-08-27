from fastapi import HTTPException
import pytest
import os

os.environ["CRYPTID_UNIT_TEST"] = "true"
from web import creature
from models.creature import Creature


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="test_creature",
        area="test_area",
        country="test_country",
        description="test_description",
        aka="test_aka",
    )


@pytest.fixture
def fakes() -> list[Creature]:
    return creature.get_all()


def assert_duplicate(exc):
    assert exc.value.status_code == 409
    assert "already exists" in exc.value.detail


def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "not found" in exc.value.detail


def test_get_all(fakes: list[Creature]):
    assert creature.get_all() == fakes


def test_create(sample: Creature):
    assert creature.create(sample) == sample


def test_create_duplicate(fakes: list[Creature]):
    with pytest.raises(HTTPException) as exc:
        creature.create(fakes[0])
    assert_duplicate(exc)


def test_get_one(sample: Creature):
    assert creature.get_one(sample.name) == sample


def test_get_one_missing():
    with pytest.raises(HTTPException) as exc:
        creature.get_one("bob")
    assert_missing(exc)


def test_modify(sample: Creature):
    sample.description = "new description"
    assert creature.modify(sample.name, sample) == sample


def test_modify_missing(fakes: list[Creature]):
    with pytest.raises(HTTPException) as exc:
        creature.modify("404", fakes[0])
    assert_missing(exc)


def test_delete(sample: Creature):
    creature.delete(sample.name)
    with pytest.raises(HTTPException) as exc:
        creature.get_one(sample.name)
    assert_missing(exc)


def test_delete_missing(sample: Creature):
    with pytest.raises(HTTPException) as exc:
        creature.delete("404")
    assert_missing(exc)
