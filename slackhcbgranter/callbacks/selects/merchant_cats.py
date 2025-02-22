from slackhcbgranter.utils.constants import MERCHANT_CATEGORIES
from thefuzz import process, fuzz

async def get_merchant_cats(payload: dict) -> list[dict[str, dict[str, str] | str]]:
    cats = MERCHANT_CATEGORIES
    keyword = payload.get("value")
    if keyword:
        cat_names = [cat["text"]["text"] for cat in cats]
        scores = process.extract(keyword, cat_names, scorer=fuzz.ratio, limit=100)
        old_cats = cats

        cats = [old_cats[cat_names.index(score[0])] for score in scores]

    return cats
