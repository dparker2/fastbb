from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from jinja2_fragments.fastapi import Jinja2Blocks

state = { "count": 0 }
app = FastAPI()
templates = Jinja2Blocks(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(
        "page.html.jinja2",
        {"request": request, "count": state["count"]}
    )


@app.put("/clicked", response_class=HTMLResponse)
def read_item(request: Request):
    state["count"] += 1
    return templates.TemplateResponse(
        "page.html.jinja2",
        {"request": request, "count": state["count"]},
        block_name="content"
    )
