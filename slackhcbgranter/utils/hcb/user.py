from slackhcbgranter.utils.hcb.requests import get
from slackhcbgranter.utils.types.hcb import User


async def get_user_data() -> User:
    response = await get("user")
    return User(
        id=response["id"],
        name=response["name"],
        email=response["email"],
        admin=response["admin"],
        avatar=response["avatar"],
    )
