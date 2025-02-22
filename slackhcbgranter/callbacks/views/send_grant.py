import logging
from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.context.ack.async_ack import AsyncAck

async def send_grant_callback(client: AsyncWebClient, ack: AsyncAck, body: dict):
    logging.info("Callback")
    view = body["view"]
    values = view["state"]["values"]
    logging.info(values)
