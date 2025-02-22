def get_modal() -> dict:
    return {
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
                "element": {"type": "email_text_input", "action_id": "email"},
                "label": {"type": "plain_text", "text": "Email", "emoji": True},
            },
            {
                "type": "input",
                "block_id": "merchant_id",
                "element": {"type": "plain_text_input"},
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
                "element": {"type": "plain_text_input"},
                "optional": True,
                "label": {"type": "plain_text", "text": "Merchant Name Regex Lock", "emoji": True},
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
            {
                "type": "input",
                "element": {"type": "rich_text_input", "action_id": "invite-message"},
                "label": {
                    "type": "plain_text",
                    "text": "Invite Message",
                    "emoji": True,
                },
            },
            {
                "type": "input",
                "element": {
                    "type": "datepicker",
                    "initial_date": "2025-04-28",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date",
                        "emoji": True,
                    },
                    "action_id": "datepicker-action",
                },
                "label": {"type": "plain_text", "text": "Expiry", "emoji": True},
            },
        ],
    }
