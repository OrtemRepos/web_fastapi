import os
import pytest
from models.user import User
from errors import Missing, Duplicate

os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from data import user as data


@pytest.fixture
def sample() -> User:
    return User(name="user1", hash="hash1")


def test_create(sample: User):
    data.create(sample)
    resp = data.get_one(sample.name)
    assert resp == sample


def test_get_all(sample: User):
    assert data.get_all() == [sample]


def test_create_duplicate(sample: User):
    with pytest.raises(Duplicate):
        data.create(sample)


def test_get_one(sample: User):
    resp = data.get_one(sample.name)
    assert resp == sample


def test_get_one_missing(sample: User):
    with pytest.raises(Missing):
        data.get_one("404")


def test_modify(sample: User):
    sample.hash = "hash2"
    resp = data.modify(sample.name, sample)
    assert resp == sample


def test_modify_missing(sample: User):
    thing: User = User(name="snurfle", hash="hash2")
    with pytest.raises(Missing):
        data.modify(thing.name, thing)


def test_delete(sample: User):
    data.delete(sample.name)
    with pytest.raises(Missing):
        data.get_one(sample.name)


def test_delete_missing(sample: User):
    with pytest.raises(Missing):
        data.delete(sample.name)
