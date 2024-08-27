import pytest
import os

os.environ["CRYPTID_UNIT_TEST"] = "true"
from models.user import User
from service import user
from errors import Missing, Duplicate


@pytest.fixture
def sample() -> User:
    return User(name="test_user", hash="test_hash")


@pytest.fixture
def fakes() -> list[User]:
    return user.get_all()


def test_get_all(fakes: list[User]):
    assert user.get_all() == fakes


def test_create(sample: User):
    assert user.create(sample) == sample


def test_create_duplicate(fakes: list[User]):
    with pytest.raises(Duplicate):
        user.create(fakes[0])


def test_get_one(sample: User):
    assert user.get_one(sample.name) == sample


def test_get_one_missing():
    with pytest.raises(Missing) as exc:
        user.get_one("bob")


def test_modify(sample: User):
    sample.hash = "hash2"
    assert user.modify(sample.name, sample) == sample


def test_modify_missing(fakes: list[User]):
    with pytest.raises(Missing):
        user.modify("404", fakes[0])


def test_delete(sample: User):
    user.delete(sample.name)
    with pytest.raises(Missing):
        user.get_one(sample.name)


def test_delete_missing(sample: User):
    with pytest.raises(Missing):
        user.delete("404")
