import os
import pytest
from models.explorer import Explorer
from errors import Missing, Duplicate

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import explorer


@pytest.fixture
def sample() -> Explorer:
    return Explorer(name="Carrigan", country="ru", description="fuck your mom")


def test_create(sample: Explorer):
    resp = explorer.create(sample)
    assert resp == sample


def test_get_all(sample: Explorer):
    resp = explorer.get_all()
    assert resp == [sample]


def test_create_duplicate(sample: Explorer):
    with pytest.raises(Duplicate):
        explorer.create(sample)


def test_get_one(sample: Explorer):
    resp = explorer.get_one(sample.name)
    assert resp == sample


def test_get_one_missing(sample: Explorer):
    with pytest.raises(Missing):
        explorer.get_one("404")


def test_modify(sample: Explorer):
    sample.country = "us"
    resp = explorer.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing(sample: Explorer):
    thing: Explorer = Explorer(name="snurfle", country="ru", description="some thing")
    with pytest.raises(Missing):
        explorer.modify(thing.name, thing)


def test_delete(sample: Explorer):
    resp = explorer.delete(sample.name)
    assert resp is None


def test_delete_missing(sample: Explorer):
    with pytest.raises(Missing):
        explorer.delete(sample.name)
