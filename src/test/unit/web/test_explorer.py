from fastapi import HTTPException
import pytest
import os

os.environ["CRYPTID_UNIT_TEST"] = "true"
from web import explorer
from models.explorer import Explorer


@pytest.fixture
def sample() -> Explorer:
    return Explorer(
        name="test_creature", country="test_country", description="test_description"
    )


@pytest.fixture
def fakes() -> list[Explorer]:
    return explorer.get_all()


def assert_duplicate(exc):
    assert exc.value.status_code == 409
    assert "already exists" in exc.value.detail


def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "not found" in exc.value.detail


def test_get_all(fakes: list[Explorer]):
    assert explorer.get_all() == fakes


def test_create(sample: Explorer):
    assert explorer.create(sample) == sample


def test_create_duplicate(fakes: list[Explorer]):
    with pytest.raises(HTTPException) as exc:
        explorer.create(fakes[0])
    assert_duplicate(exc)


def test_get_one(sample: Explorer):
    assert explorer.get_one(sample.name) == sample


def test_get_one_missing():
    with pytest.raises(HTTPException) as exc:
        explorer.get_one("bob")
    assert_missing(exc)


def test_modify(sample: Explorer):
    sample.description = "new description"
    assert explorer.modify(sample.name, sample) == sample


def test_modify_missing(fakes: list[Explorer]):
    with pytest.raises(HTTPException) as exc:
        explorer.modify("404", fakes[0])
    assert_missing(exc)


def test_delete(sample: Explorer):
    explorer.delete(sample.name)
    with pytest.raises(HTTPException) as exc:
        explorer.get_one(sample.name)
    assert_missing(exc)


def test_delete_missing(sample: Explorer):
    with pytest.raises(HTTPException) as exc:
        explorer.delete("404")
    assert_missing(exc)
