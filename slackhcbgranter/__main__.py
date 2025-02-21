import asyncio
import contextlib
import logging

import uvicorn
import uvloop
from dotenv import load_dotenv
from starlette.applications import Starlette

from slackhcbgranter.utils.env import env


load_dotenv()

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logging.basicConfig(level="INFO")


@contextlib.asynccontextmanager
async def main(_app: Starlette):
    # await authorise()
    yield


def start():
    uvicorn.run(
        "slackhcbgranter.utils.starlette:app",
        host="0.0.0.0",
        port=env.port,
        log_level="info",
    )


if __name__ == "__main__":
    start()
