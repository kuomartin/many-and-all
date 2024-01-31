from math import sqrt


from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


@form_body
class Many(BaseModel):
    cloth: bool = True
    time: int = 0


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse("/many-and-all")


@app.post('/many-and-all', response_class=HTMLResponse)
async def main(request: Request,item: Many):
    price = getPrice(item.time, item.cloth)
    return templates.TemplateResponse(name="price.html", context={'request': request,'price':price})


@app.get("/many-and-all", response_class=HTMLResponse)
async def manyAndAll(request: Request):
    return templates.TemplateResponse(name="main.html", context={'request': request})


def getPrice(time: int = 0, cloth: bool = True):
    p = sqrt((2 / 9) * time ** 2 + 340 / 3 * time)
    if not cloth:
        p *= 2
    return p
