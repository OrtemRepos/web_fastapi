import os

from pydantic import Field
from fastapi import APIRouter, HTTPException, Response
import plotly.express as px
import country_converter as coco
from collections import Counter
from string import ascii_uppercase
from models.creature import Creature

if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import creature as service
else:
    import service.creature as service
from errors import Missing, Duplicate

router = APIRouter(prefix="/creature")


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()[:5]


@router.get("/{name}")
def get_one(name: str) -> Creature | None:
    try:
        return service.get_one(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/")
def modify(name: str, creature: Creature) -> Creature:
    try:
        return service.modify(name, creature)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("/{name}", status_code=204)
def delete(name: str) -> None:
    try:
        return service.delete(name)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)

@router.get("/plot/")
def plot() -> Response:
    creatures = service.get_all()
    letters = ascii_uppercase
    counts = Counter(c.name[0] for c in creatures)
    y = {letter: counts.get(letter, 0) for letter in letters}
    fig = px.histogram(x=list(letters), y=y, title="Creature Names",
                       labels={"x": "Intitial", "y": "Initial"})
    fig_bytes = fig.to_image(format="png")
    return Response(content=fig_bytes, media_type="image/png")

@router.get("/map/")
def map() -> Response:
    creatures = service.get_all()
    iso2_codes = set(creature.country for creature in creatures)
    iso3_codes = coco.convert(names=iso2_codes, to="ISO3")
    fig = px.choropleth(
        locationmode='ISO-3',
        locations=iso3_codes
    )
    fog_bytes = fig.to_image(format="png")
    return Response(content=fog_bytes, media_type="image/png")