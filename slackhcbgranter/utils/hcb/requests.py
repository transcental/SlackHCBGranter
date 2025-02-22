from aiohttp import ClientSession

from slackhcbgranter.utils.env import env


async def get(endpoint: str) -> dict:
    async with ClientSession() as session:
        async with session.get(
            f"{env.hcb_base_url}/api/v4/{endpoint}",
            headers={"Authorization": f"Bearer {env.hcb_token}"},
        ) as response:
            return await response.json()
