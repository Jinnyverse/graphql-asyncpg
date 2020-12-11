from aiohttp import web
import asyncpg
from graphql import graphql
from schema import schema


async def init(app):
    app["db"] = await asyncpg.create_pool(user="postgres", password="pass", database="dummy")


async def get_query(request):
    content_type = request.content_type
    if content_type == "application/graphql":
        return await request.text()
    elif content_type == "application/json":
        return (await request.json())["query"]


async def playground(request):
    query = await get_query(request)
    result = await graphql(schema, query, context_value={"db": request.app["db"]})
    errors = result.errors
    if errors:
        errors = [error.formatted for error in errors]
        result = {"errors": errors}
    else:
        result = {"data": result.data}
    return web.json_response(result)

app = web.Application()
app.on_startup.append(init)
app.router.add_post("/graphql", playground)
web.run_app(app, port=8000)
