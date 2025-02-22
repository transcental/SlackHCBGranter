from slackhcbgranter.utils.hcb.requests import get


async def create_grant(
    org: str,
    amount: float,
    email: str,
    merchant_id: str,
    merchant_cats: list[str],
    merchant_regex: str,
    purpose: str,
):
    res = await get(
        f"card_grants/create?event_id={org}&amount_cents={int(amount * 100)}&email={email}&merchant_lock={merchant_id}&category_lock={merchant_cats}&keyword_lock={merchant_regex}&purpose={purpose}"
    )
    return res
