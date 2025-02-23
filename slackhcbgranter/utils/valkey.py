import json
import time
from typing import Optional

from valkey.asyncio import Valkey

from slackhcbgranter.utils.hcb.organisations import get_eligible_orgs
from slackhcbgranter.utils.hcb.user import get_user_data
from slackhcbgranter.utils.types.valkey import User


class ValkeyClient:
    def __init__(self, host: str, port: int, db: int) -> None:
        self.r = Valkey(
            host=host,
            port=port,
            db=db,
        )

    async def get_user(self, user_id: str) -> User | None:
        data = await self.r.get(f"user:{user_id}")
        if data:
            return User(**json.loads(data))
        return None

    async def cache_user(self, user_id: str, token: Optional[str] = None) -> User:
        user = await self.get_user(user_id)
        if not user:
            user_data = await get_user_data()
            organisations = await get_eligible_orgs()
            ids = [org.id for org in organisations]
            current_time = int(time.time())
            expiry = current_time + 86400
            user = User(
                id=user_data.id,
                name=user_data.name,
                email=user_data.email,
                admin=user_data.admin,
                avatar=user_data.avatar,
                token=token,
                expiresAt=expiry,
                organisations=ids,
            )
        await self.r.set(f"user:{user_id}", "1")
        return user

    async def get(self, key: str) -> str:
        return await self.r.get(key)

    async def set(self, key: str, value: str) -> None:
        await self.r.set(key, value)

    async def delete(self, key: str) -> None:
        await self.r.delete(key)

    async def close(self) -> None:
        await self.r.aclose()
