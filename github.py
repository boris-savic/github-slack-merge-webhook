import hmac

from fastapi import Request, HTTPException
from starlette.status import HTTP_403_FORBIDDEN

from config import settings


async def verify_github_signature(req: Request):
    signature = req.headers.get('x-hub-signature-256')
    if not settings.github_verify_signature:
        return

    if not signature:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authorized")

    valid = await verify_signature(message=await req.body(), signature=signature, secret=settings.github_webhook_secret)

    if not valid:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid signature")


async def verify_signature(message: bytes, signature: str, secret: str) -> bool:
    return signature == await calculate_signature(message=message, secret=secret)


async def calculate_signature(message: bytes, secret: str) -> str:
    return f"sha256={hmac.new(key=secret.encode('utf-8'), msg=message, digestmod='sha256').hexdigest()}"
