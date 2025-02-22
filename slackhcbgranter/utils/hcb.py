import asyncio
from aiohttp import ClientSession
from slackhcbgranter.utils.env import env
from slackhcbgranter.utils.types.hcb import OrgUser, Organisation, User


async def get(endpoint: str) -> dict:
    async with ClientSession() as session:
        async with session.get(
            f"{env.hcb_base_url}/api/v4/{endpoint}",
            headers={"Authorization": f"Bearer {env.hcb_token}"},
        ) as response:
            return await response.json()


async def get_orgs() -> list[Organisation]:
    response = await get("user/organizations")
    orgs = await asyncio.gather(*[get_org(org["id"]) for org in response])
    return orgs


async def get_org(org_id: str) -> Organisation:
    response = await get(f"organizations/{org_id}")
    org = Organisation(
        id=response["id"],
        slug=response["slug"],
        name=response["name"],
        icon=response.get("icon"),
        playground_mode=response.get("playground_mode", True),
        balance=response.get("balance_cents", 0)/100,
        users=[
            OrgUser(
                id=user["id"],
                name=user["name"],
                email=user["email"],
                admin=user["admin"],
                avatar=user["avatar"],
                role=user.get("role", "Member"),
            )
            for user in response["users"]
        ],
    )
    return org


async def get_eligible_orgs() -> list[Organisation]:
    raw_orgs = await get_orgs()
    orgs = [await get_org(org.id) for org in raw_orgs]
    user_data = await get_user_data()
    eligible_orgs = [org for org in orgs if not org.playground_mode and any(((user.id == user_data.id and user.role == "manager") or user_data.admin) for user in org.users)]
    return eligible_orgs


async def get_user_data() -> User:
    response = await get("user")
    return User(
        id=response["id"],
        name=response["name"],
        email=response["email"],
        admin=response["admin"],
        avatar=response["avatar"],
    )
