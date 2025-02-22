from aiohttp import ClientSession

from slackhcbgranter.utils.env import env
from slackhcbgranter.utils.types.requests import Response


async def get(endpoint: str) -> Response:
    async with ClientSession() as session:
        async with session.get(
            f"{env.hcb_base_url}/api/v4/{endpoint}",
            headers={"Authorization": f"Bearer {env.hcb_token}"},
        ) as response:
            content = await response.text()
            return Response(response.status, response.headers, content)


async def post(endpoint: str, data: dict) -> Response:
    async with ClientSession() as session:
        async with session.post(
            f"{env.hcb_base_url}/api/v4/{endpoint}",
            headers={"Authorization": f"Bearer {env.hcb_token}"},
            json=data,
        ) as response:
            content = await response.text()
            return Response(response.status, response.headers, content)
