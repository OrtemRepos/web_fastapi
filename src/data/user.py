from models.user import User
from .__init__ import conn, curs, IntegrityError
from errors import Missing, Duplicate

curs.execute(
    """create table if not exists
             user(
             name text primary key,
             hash text
             )"""
)

curs.execute(
    """create table if not exists
             xuser(
             name text primary key,
             hash text
             )"""
)


def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name=name, hash=hash)


def model_to_dict(user: User) -> dict:
    return user.model_dump()


def get_one(name: str) -> User:
    qry = "select * from user where name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"User {name} not found")


def get_all() -> list[User]:
    qry = "select * from user"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]


def create(user: User, table: str = "user") -> None:
    qry = f"""insert into {table} values (:name, :hash)"""
    params = model_to_dict(user)
    try:
        curs.execute(qry, params)
    except IntegrityError:
        raise Duplicate(msg=f"User {user.name} already exists")


def modify(name: str, user: User) -> User:
    qry = """update user set name=:name, hash=:hash where name=:name_orig"""
    params = {"name": user.name, "hash": user.hash, "name_orig": name}
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return get_one(user.name)
    else:
        raise Missing(msg=f"User {name} not found")


def delete(name: str) -> None:
    user = get_one(name)
    qry = "delete from user where name=:name"
    params = {"name": name}
    res = curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"User {name} not found")
    create(user, table="xuser")
