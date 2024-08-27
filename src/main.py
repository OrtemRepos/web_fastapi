from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from web import explorer, creature, user
from pathlib import Path

app = FastAPI()

app = FastAPI()
top = Path(__file__).resolve().parent
template_obj = Jinja2Templates(directory=f"{top}/template")

from fake.creature import fakes as fake_creatures
from fake.explorer import fakes as fake_explorers


@app.get("/list")
def explorer_list(request: Request):
    return template_obj.TemplateResponse(
        "list.html",
        {"request": request, "creatures": fake_creatures, "explorers": fake_explorers},
    )


app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
