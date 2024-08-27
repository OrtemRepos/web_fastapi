from .__init__ import conn, curs, IntegrityError
from models.creature import Creature
from errors import Missing, Duplicate

curs.execute(
    """
    create table if not exists creature(
             name text primary key,
             country text,
             area text,
             description text,
             aka text)
    """
)


def row_to_model(row: tuple) -> Creature:
    name, country, area, description, aka = row
    return Creature(
        name=name, country=country, area=area, description=description, aka=aka
    )


def model_to_dict(model: Creature):
    return model.model_dump()


def get_one(name: str) -> Creature:
    qry = "select * from creature where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Creature {name} not found")


def get_all() -> list[Creature]:
    qry = "select * from creature"
    curs.execute(qry)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]


def create(creature: Creature) -> None:
    qry = "insert into creature values (:name, :country, :area, :description, :aka)"
    params = model_to_dict(creature)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"Creature {creature.name} already exists")
    return get_one(creature.name)


def modify(name: str, creature: Creature) -> Creature | None:
    if not (name and creature):
        return None
    qry = "update creature set name=:name, country=:country, area=:area, description=:description, aka=:aka where name=:name_orig"
    params = model_to_dict(creature)
    params["name_orig"] = name
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return get_one(creature.name)
    else:
        raise Missing(msg=f"Creature {name} not found")


def delete(name: str) -> bool | None:
    if not name:
        return False
    qry = "delete from creature where name=:name"
    params = {"name": name}
    res = curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Creature {name} not found")
