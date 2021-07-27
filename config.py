from pydantic import BaseSettings

from slack import SLACK_PAYLOAD


class Settings(BaseSettings):
    """
    Reads configurations from ENV variables.
    """
    slack_url: str = None
    github_verify_signature: bool = False
    github_webhook_secret: str = "secret-key"
    slack_message: str = SLACK_PAYLOAD

settings = Settings()
