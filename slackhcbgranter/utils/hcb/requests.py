from aiohttp import ClientSession

from slackhcbgranter.utils.env import env


async def get(endpoint: str) -> dict:
    async with ClientSession() as session:
        async with session.get(
            f"{env.hcb_base_url}/api/v4/{endpoint}",
            headers={"Authorization": f"Bearer {env.hcb_token}"},
        ) as response:
            return await response.json()


async def post(endpoint: str, data: dict) -> dict:
    async with ClientSession() as session:
        async with session.post(
            f"{env.hcb_base_url}/api/v4/{endpoint}",
            headers={"Authorization": f"Bearer {env.hcb_token}"},
            json=data,
        ) as response:
            return await response.json()
