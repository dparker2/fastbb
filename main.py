import sqlite3
from typing_extensions import Annotated
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from jinja2_fragments.fastapi import Jinja2Blocks


def get_db():
    conn = sqlite3.connect("data.db")
    try:
        yield conn
    finally:
        conn.close()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


state = {"count": 0}
app = FastAPI(lifespan=lifespan)
templates = Jinja2Blocks(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, conn: Annotated[sqlite3.Connection, Depends(get_db)]):
    posts = list(
        map(
            lambda row: {"user": row[0], "content": row[1]},
            conn.execute("SELECT user, content FROM posts"),
        )
    )
    print(posts)

    return templates.TemplateResponse(
        "page.html.jinja2", {"request": request, "posts": posts}
    )


@app.post("/posts", response_class=HTMLResponse)
def make_post(
    request: Request,
    user: Annotated[str, Form()],
    content: Annotated[str, Form()],
    conn: Annotated[sqlite3.Connection, Depends(get_db)],
):
    conn.execute("INSERT INTO posts (user, content) VALUES (?,?)", [user, content])
    conn.commit()
    print(user, content)

    return templates.TemplateResponse(
        "page.html.jinja2",
        {"request": request, "posts": [{"user": user, "content": content}]},
        block_name="post",
    )
