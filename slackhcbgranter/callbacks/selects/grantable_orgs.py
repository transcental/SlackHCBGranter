from thefuzz import fuzz
from thefuzz import process

from slackhcbgranter.utils.hcb.organisations import get_eligible_orgs


async def get_grantable_orgs(payload: dict) -> list[dict[str, dict[str, str] | str]]:
    orgs = await get_eligible_orgs()
    keyword = payload.get("value")
    if keyword:
        org_names = [org.name for org in orgs]
        scores = process.extract(keyword, org_names, scorer=fuzz.ratio, limit=100)
        old_orgs = orgs

        orgs = [old_orgs[org_names.index(score[0])] for score in scores]
    return [
        {
            "text": {"type": "plain_text", "text": f"{org.name} (${org.balance})"},
            "value": org.id,
        }
        for org in orgs
    ]
