import os

from dotenv import load_dotenv
from slack_sdk.web.async_client import AsyncWebClient

load_dotenv()


class Environment:
    def __init__(self):
        self.slack_bot_token = os.getenv("SLACK_BOT_TOKEN", "unset")
        self.slack_signing_secret = os.getenv("SLACK_SIGNING_SECRET", "unset")

        self.hcb_client_id = os.getenv("HCB_CLIENT_ID", "unset")
        self.hcb_client_secret = os.getenv("HCB_CLIENT_SECRET", "unset")
        self.hcb_redirect_uri = os.getenv("HCB_REDIRECT_URI", "unset")
        self.hcb_base_url = os.getenv("HCB_BASE_URL", "unset")
        self.environment = os.getenv("ENVIRONMENT", "development")

        unset = [key for key, value in self.__dict__.items() if value == "unset"]
        if unset:
            raise Exception(f"Environment variables {unset} not set")

        self.port = int(os.environ.get("PORT", 8000))
        self.slack_client = AsyncWebClient(token=self.slack_bot_token)
        self.hcb_state = ""
        self.hcb_token = ""
        self.slack_user_ids = ["U054VC2KM9P"]


env = Environment()
