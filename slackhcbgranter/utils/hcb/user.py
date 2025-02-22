import json

from slackhcbgranter.utils.hcb.requests import get
from slackhcbgranter.utils.types.hcb import User


async def get_user_data() -> User:
    response = await get("user")
    response = json.loads(response.content)
    return User(
        id=response["id"],
        name=response["name"],
        email=response["email"],
        admin=response["admin"],
        avatar=response["avatar"],
    )
