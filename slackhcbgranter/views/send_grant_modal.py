from typing import Optional


def get_modal(
    message: Optional[str] = None, inital_values: Optional[dict] = None
) -> dict:
    view = {
        "type": "modal",
        "title": {"type": "plain_text", "text": "Send Grant", "emoji": True},
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        "callback_id": "send_grant",
        "blocks": [
            {
                "type": "input",
                "block_id": "organisation",
                "element": {
                    "action_id": "grantable_orgs",
                    "type": "external_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Choose an organisation",
                    },
                    "min_query_length": 0,
                },
                "label": {"type": "plain_text", "text": "Organisation", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "email",
                "element": {"type": "email_text_input", "action_id": "email"},
                "label": {"type": "plain_text", "text": "Email", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "balance",
                "element": {
                    "type": "number_input",
                    "is_decimal_allowed": True,
                    "action_id": "balance",
                    "min_value": "0.1",
                    "max_value": "2147483647",
                },
                "label": {"type": "plain_text", "text": "Amount (USD)", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "purpose",
                "element": {"type": "plain_text_input", "action_id": "purpose"},
                "optional": True,
                "label": {
                    "type": "plain_text",
                    "text": "Purpose",
                    "emoji": True,
                },
            },
            {
                "type": "input",
                "block_id": "merchant_id",
                "element": {"type": "plain_text_input", "action_id": "merchant_id"},
                "optional": True,
                "label": {
                    "type": "plain_text",
                    "text": "Merchant ID Lock",
                    "emoji": True,
                },
            },
            {
                "type": "input",
                "block_id": "regex",
                "element": {"type": "plain_text_input", "action_id": "merchant_regex"},
                "optional": True,
                "label": {
                    "type": "plain_text",
                    "text": "Merchant Name Regex Lock",
                    "emoji": True,
                },
            },
            {
                "type": "input",
                "block_id": "merchant_category",
                "element": {
                    "action_id": "merchant_cats",
                    "type": "multi_external_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Choose categories to lock to",
                    },
                    "min_query_length": 0,
                },
                "optional": True,
                "label": {"type": "plain_text", "text": "Category Lock", "emoji": True},
            },
        ],
    }

    if inital_values:
        if inital_values["organisation"]:
            view["blocks"][0]["element"]["initial_option"] = inital_values[
                "organisation"
            ]

        view["blocks"][1]["element"]["initial_value"] = inital_values["email"] or ""
        view["blocks"][2]["element"]["initial_value"] = inital_values["balance"] or ""
        view["blocks"][3]["element"]["initial_value"] = inital_values["purpose"] or ""
        view["blocks"][4]["element"]["initial_value"] = (
            inital_values["merchant_id"] or ""
        )
        view["blocks"][5]["element"]["initial_value"] = (
            inital_values["merchant_regex"] or ""
        )
        view["blocks"][6]["element"]["initial_options"] = (
            inital_values["merchant_cats"] or []
        )

    if message:
        view["blocks"].insert(
            0, {"type": "section", "text": {"type": "mrkdwn", "text": message}}
        )

    return view
