import json
import logging
import re

from slack_bolt.context.ack.async_ack import AsyncAck
from slack_sdk.web.async_client import AsyncWebClient

from slackhcbgranter.utils.hcb.grants import create_grant
from slackhcbgranter.utils.hcb.organisations import get_org
from slackhcbgranter.views.send_grant_modal import get_modal


async def send_grant_callback(client: AsyncWebClient, ack: AsyncAck, body: dict):
    logging.info("Callback")
    view = body["view"]
    values = view["state"]["values"]
    org = (
        values.get("organisation", {})
        .get("grantable_orgs", {})
        .get("selected_option", {})
        .get("value")
    )

    if not org:
        return await ack(
            {
                "response_action": "errors",
                "errors": {"organisation": "Organisation cannot be empty"},
            }
        )

    balance = values.get("balance", {}).get("balance", {}).get("value")
    if not balance:
        return await ack(
            {
                "response_action": "errors",
                "errors": {"balance": "Amount cannot be empty"},
            }
        )
    balance = float(balance)
    if balance <= 0:
        return await ack(
            {
                "response_action": "errors",
                "errors": {"balance": "Amount must be greater than $0"},
            }
        )
    elif balance > 2147483647:
        return await ack(
            {
                "response_action": "errors",
                "errors": {"balance": "Amount must be less than $2147483647"},
            }
        )
    elif balance % 0.01 != 0:
        return await ack(
            {
                "response_action": "errors",
                "errors": {"balance": "Amount must be a multiple of $0.01"},
            }
        )

    email = values.get("email", {}).get("email", {}).get("value")

    if not email:
        return await ack(
            {"response_action": "errors", "errors": {"email": "Email cannot be empty"}}
        )
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(email_regex, email):
        return await ack(
            {"response_action": "errors", "errors": {"email": "Invalid email"}}
        )

    merchant_id = values.get("merchant_id", {}).get("merchant_id", {}).get("value")
    merchant_regex = values.get("regex", {}).get("merchant_regex", {}).get("value")
    merchant_cats = [
        merchant.get("value")
        for merchant in values.get("merchant_category", {})
        .get("merchant_cats", {})
        .get("selected_options", [])
    ]

    purpose = values.get("purpose", {}).get("purpose", {}).get("value")

    logging.info(
        f"Creating grant for {org} with balance {balance} for {email} with merchant_id {merchant_id} and merchant_cats {merchant_cats} and merchant_regex {merchant_regex} with purpose {purpose}"
    )
    res = await create_grant(
        org, balance, email, merchant_id, merchant_cats, merchant_regex, purpose
    )
    mimetype = res.headers.get("Content-Type", "")
    if "application/json" not in mimetype:
        logging.info(f"Error creating grant: {res.content}")
        view = get_modal(
            "*Unknown error whilst creating grant*\nSomething really went wrong here, if this continues to happen, DM <@U054VC2KM9P>."
        )
        return await ack(response_action="update", view=view)
    data = json.loads(res.content)
    if data.get("error"):
        initial_values = {
            "organisation": values.get("organisation", {})
            .get("grantable_orgs", {})
            .get("selected_option", {}),
            "email": values.get("email", {}).get("email", {}).get("value", ""),
            "balance": values.get("balance", {})
            .get("balance", {})
            .get("value", "5.00"),
            "purpose": values.get("purpose", {}).get("purpose", {}).get("value", ""),
            "merchant_id": values.get("merchant_id", {})
            .get("merchant_id", {})
            .get("value", ""),
            "merchant_regex": values.get("regex", {})
            .get("merchant_regex", {})
            .get("value", ""),
            "merchant_cats": values.get("merchant_category", {})
            .get("merchant_cats", {})
            .get("selected_options", []),
        }
        message = f"*Error creating grant*\n`{data.get('error')}`"
        if data.get("message"):
            message += f"- {data.get('message')}"
        view = get_modal(message, initial_values)
        await ack(response_action="update", view=view)
    elif data.get("status") == "active":
        await ack()
        org = await get_org(org)
        restrictions = ""
        if merchant_id:
            restrictions += f"\nAllowed Merchants: {merchant_id}"
        if merchant_cats:
            restrictions += f"\nAllowed Merchant Categories: {','.join(merchant_cats)}"
        if merchant_regex:
            restrictions += f"\nAllowed Merchant Regex: {merchant_regex}"
        if purpose:
            restrictions += f"\nPurpose: {purpose}"
        await client.chat_postMessage(
            channel=body["user"]["id"],
            text=f"Issued ${balance:.2f} grant for {email} from {org.name}.\n{restrictions}",
        )
