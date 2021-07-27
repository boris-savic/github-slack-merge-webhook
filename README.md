# Github to Slack Notifier


## Running project

```bash
uvicorn main:app --reload --port 9000
```

## Docker Support

```bash
docker-compose up --build
```


## Environment Variables

The project reads configuration from the environment variables. 

```
# Slack Hooks https://api.slack.com/messaging/webhooks
SLACK_URL=<url-of-the-slack-webhook>
SLACK_MESSAGE=<slack-formatted-message-to-send>

# Verify Github Webhook Signature
GITHUB_VERIFY_SIGNATURE=False
GITHUB_WEBHOOK_SECRET=<secret-key>
```

### Default Slack Message

In the message we send to slack we encode the following variables:

  - `author`
  - `title`
  - `description` 
  - `html_url`

The JSON you wish to send to Slack (`SLACK_MESSAGE`) can be changed via environment variable. 
Make sure the JSON string is properly escaped. 

For example a simple text message as below:
```json
{
    "text": "Merged {title}"
}
```

Must be escaped as the following example:
```
{{"text": "Merged {title}"}}
```
