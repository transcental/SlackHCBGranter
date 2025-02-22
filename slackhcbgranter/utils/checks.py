from slack_bolt.context.ack.async_ack import AsyncAck
from slackhcbgranter.utils.env import env
from slackhcbgranter.utils.oauth import authorise

async def check_auth(ack: AsyncAck, user_id: str) -> bool:
    await ack()
    if user_id not in env.slack_user_ids:
        await ack("You are not authorised to use this yet :(")
        return False
    elif env.hcb_token == "":
        url = await authorise()
        await ack(f"<{url}|Login to HCB> first")
        return False
    else:
        return True
