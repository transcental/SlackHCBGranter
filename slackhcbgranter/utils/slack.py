from slack_bolt.async_app import AsyncApp
from slack_bolt.context.ack.async_ack import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from slackhcbgranter.commands.send_grant import send_grant_callback
from slackhcbgranter.utils.env import env
from slackhcbgranter.utils.oauth import authorise

app = AsyncApp(
    token=env.slack_bot_token,
    signing_secret=env.slack_signing_secret,
)


@app.command("/hcb-send-grant")
async def send_grant(client: AsyncWebClient, ack: AsyncAck, body: dict):
    await send_grant_callback(client, ack, body)


@app.command("/hcb-login")
async def login(client: AsyncWebClient, ack: AsyncAck):
    url = await authorise()
    await ack(f"<{url}|Login to HCB>")
