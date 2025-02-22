import asyncio

from slackhcbgranter.utils.hcb.requests import get
from slackhcbgranter.utils.hcb.user import get_user_data
from slackhcbgranter.utils.types.hcb import Organisation
from slackhcbgranter.utils.types.hcb import OrgUser


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
        balance=response.get("balance_cents", 0) / 100,
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
    eligible_orgs = [
        org
        for org in orgs
        if not org.playground_mode
        and any(
            ((user.id == user_data.id and user.role == "manager") or user_data.admin)
            for user in org.users
        )
    ]
    return eligible_orgs
