import binascii
import os

from aiohttp import ClientSession
from starlette.requests import Request
from starlette.responses import JSONResponse

from slackhcbgranter.utils.env import env


async def authorise():
    signature = binascii.hexlify(os.urandom(32))
    state = signature.decode("utf-8")
    env.hcb_state = state

    hcb_url = f"{env.hcb_base_url}/api/v4/oauth/authorize?client_id={env.hcb_client_id}&redirect_uri={env.hcb_redirect_uri}&response_type=code&scope=write%20read&state={state}"

    return hcb_url


async def callback(req: Request):
    code = req.query_params.get("code", "")
    state = req.query_params.get("state")
    if state != env.hcb_state:
        return JSONResponse({"error": "Invalid state"})

    async with ClientSession() as session:
        async with session.post(
            f"{env.hcb_base_url}/api/v4/oauth/token",
            data={
                "client_id": env.hcb_client_id,
                "client_secret": env.hcb_client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": env.hcb_redirect_uri,
            },
        ) as response:
            json = await response.json()
            env.hcb_token = json["access_token"]
    return JSONResponse({"message": "Authorised"})
