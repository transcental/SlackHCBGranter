from slack_bolt.adapter.starlette.async_handler import AsyncSlackRequestHandler
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from slackhcbgranter.__main__ import main
from slackhcbgranter.utils.env import env
from slackhcbgranter.utils.hcb.oauth import callback as hcb_callback
from slackhcbgranter.utils.slack import app as slack_app

req_handler = AsyncSlackRequestHandler(slack_app)


async def endpoint(req: Request):
    return await req_handler.handle(req)


async def health(req: Request):
    return JSONResponse({"healthy": True})


app = Starlette(
    debug=True if env.environment != "production" else False,
    routes=[
        Route(path="/slack/events", endpoint=endpoint, methods=["POST"]),
        Route(path="/health", endpoint=health, methods=["GET"]),
        Route(path="/hcb/redirect", endpoint=hcb_callback, methods=["GET"]),
    ],
    lifespan=main,
)
