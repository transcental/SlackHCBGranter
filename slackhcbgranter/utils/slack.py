from slack_bolt.async_app import AsyncApp
from slack_bolt.context.ack.async_ack import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from slackhcbgranter.callbacks.commands.send_grant import (
    send_grant_callback as send_grant_cmd_callback,
)
from slackhcbgranter.callbacks.selects.grantable_orgs import get_grantable_orgs
from slackhcbgranter.callbacks.selects.merchant_cats import get_merchant_cats
from slackhcbgranter.callbacks.views.send_grant import (
    send_grant_callback as send_grant_view_callback,
)
from slackhcbgranter.utils.checks import check_auth
from slackhcbgranter.utils.env import env

app = AsyncApp(
    token=env.slack_bot_token,
    signing_secret=env.slack_signing_secret,
)


@app.command("/hcb-send-grant")
async def send_grant(client: AsyncWebClient, ack: AsyncAck, body: dict):
    status = await check_auth(ack, body["user_id"])
    if status:
        await send_grant_cmd_callback(client, ack, body)


@app.options("grantable_orgs")
async def grantable_orgs(payload: dict, ack: AsyncAck):
    orgs = await get_grantable_orgs(payload)
    await ack(options=orgs)


@app.options("merchant_cats")
async def merchant_cats(payload: dict, ack: AsyncAck):
    cats = await get_merchant_cats(payload)
    await ack(options=cats)


@app.view("send_grant")
async def send_grant_view(client: AsyncWebClient, ack: AsyncAck, body: dict):
    await send_grant_view_callback(client, ack, body)
