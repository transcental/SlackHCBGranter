import binascii
import os

from starlette.requests import Request
from starlette.responses import JSONResponse

from slackhcbgranter.utils.env import env


async def authorise():
    signature = binascii.hexlify(os.urandom(32))
    state = signature.decode("utf-8")
    env.hcb_state = state

    hcb_url = f"{env.hcb_base_url}/api/v4/oauth/authorize?client_id={env.hcb_client_id}&redirect_uri={env.hcb_redirect_uri}&response_type=code&scope=write;read&state={state}"

    return hcb_url


async def callback(req: Request):
    code = req.query_params.get("code", "")
    state = req.query_params.get("state")
    if state != env.hcb_state:
        return JSONResponse({"error": "Invalid state"})

    print(code)
    env.hcb_code = code
    return JSONResponse({"message": "Authorised"})
