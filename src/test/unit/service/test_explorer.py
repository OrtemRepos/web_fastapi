import os
from models.explorer import Explorer
from errors import Missing, Duplicate
import pytest

os.environ["CRYPTID_UNIT_TEST"] = "true"
from service import explorer as code


@pytest.fixture
def sample() -> Explorer:
    return Explorer(name="Carrigan", country="ru", description="fuck your mom")


def test_create(sample: Explorer):
    resp = code.create(sample)
    assert resp == sample


def test_create_duplicate(sample: Explorer):
    with pytest.raises(Duplicate):
        code.create(sample)


def test_get_exists(sample: Explorer):
    resp = code.get_one(sample.name)
    assert resp == sample


def test_get_not_exists(sample: Explorer):
    with pytest.raises(Missing):
        code.get_one("Snowman")


def test_modify(sample: Explorer):
    sample.description = "loser"
    resp = code.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing(sample: Explorer):
    with pytest.raises(Missing):
        code.modify("Snowman", sample)


def test_delete(sample: Explorer):
    resp = code.delete(sample.name)
    assert resp is None


def test_delete_missing(sample: Explorer):
    with pytest.raises(Missing):
        code.delete("Snowman")
