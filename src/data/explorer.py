from .__init__ import conn, curs, IntegrityError
from models.explorer import Explorer
from errors import Missing, Duplicate

curs.execute(
    """
    create table if not exists explorer(
             name text primary key,
             country text,
             description text)
"""
)


def row_to_model(row: tuple) -> Explorer:
    (name, country, description) = row
    return Explorer(name=name, country=country, description=description)


def model_to_dict(model: Explorer) -> dict:
    return model.model_dump()


def get_one(name: str) -> Explorer | None:
    qry = "select * from explorer where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found")


def get_all() -> list[Explorer] | None:
    qry = "select * from explorer"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(explorer: Explorer) -> None:
    if not explorer:
        return None
    qry = "insert into explorer values (:name, :country, :description)"
    params = model_to_dict(explorer)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"Explorer {explorer.name} already exists")
    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    if not (name and explorer):
        return None
    qry = "update explorer set name=:name, country=:country, description=:description where name=:name_orig"
    params = model_to_dict(explorer)
    params["name_orig"] = name
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return get_one(explorer.name)
    else:
        raise Missing(msg=f"Explorer {name} not found")


def delete(name: str) -> bool | None:
    if not name:
        return False
    qry = "delete from explorer where name=:name"
    params = {"name": name}
    res = curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"Explorer {name} not found")
