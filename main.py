import httpx
import json

from config import settings

from fastapi import FastAPI, Request, Depends
from github import verify_github_signature


app = FastAPI(
    title="Slack Github Merge Webhook",
    description="Posts a message to Slack when a Pull Request is merged.",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Hello Worlds"}


@app.post("/github/webhook", dependencies=[Depends(verify_github_signature)])
async def handle_github_webhook(req: Request):
    # Fetch Github Event Type
    event_type = req.headers.get("X-Github-Event")

    # Only respond on pull_request events.
    # Docs: https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads#pull_request
    if event_type == 'pull_request':
        data = await req.json()

        # We're only interested in closed and merged changes
        if data.get('action') == 'closed' and data.get('pull_request', {}).get('merged'):
            author = data['pull_request']['user']['login']
            title = data['pull_request']['title']
            description = data['pull_request']['body']
            html_url = data['pull_request']['html_url']

            slack_message = settings.slack_message.format(author=author,
                                                          title=title,
                                                          description=description,
                                                          html_url=html_url)

            httpx.post(url=settings.slack_url, data=json.loads(slack_message))

    return {"success": True}
