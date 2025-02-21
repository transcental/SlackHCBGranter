from slack_bolt.context.ack.async_ack import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from slackhcbgranter.views.send_grant_modal import get_modal


async def send_grant_callback(client: AsyncWebClient, ack: AsyncAck, body: dict):
    await ack()
    await client.views_open(
        view=get_modal(),
        trigger_id=body["trigger_id"],
    )
