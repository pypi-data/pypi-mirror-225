import logging
import os
from typing import Annotated

from fastapi import FastAPI, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth2Session
import sentry_sdk

from .config import read_config_file, fetch_openid_config
from .oauth2_client import OAuth2Client


logging.basicConfig(level=logging.INFO)

config = read_config_file(path=os.environ.get("CONFIG_FILE", "./config.yaml"))
dex_config = fetch_openid_config(config.oidc.url)


if (sentry_dsn := os.environ.get("SENTRY_DSN")) is not None:
    sentry_sdk.init(sentry_dsn)
    logging.info("Sentry enabled")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
)

oauth2_client = OAuth2Client(
    oidc_config=config.oidc,
    dex_config=dex_config,
    redirect_uri=f"{config.api.url.rstrip('/')}/auth/v1/callback",
)


@app.get("/v1/login")
def v1_login() -> str:
    secure = config.api.url.startswith("https")
    login_url, state = oauth2_client.authorization_url(scope=["openid", "email"])

    response = RedirectResponse(login_url)
    response.set_cookie(
        "original_state",
        value=state,
        max_age=60 * 5,
        httponly=True,
        samesite="lax",
        secure=secure,
    )
    return response


@app.get("/v1/callback")
def v1_callback(
    response: Response,
    code: str,
    state: str,
    original_state: Annotated[str | None, Cookie()] = None,
):
    secure = config.api.url.startswith("https")
    if original_state is None:
        response.status_code = 400
        return "Missing original_state cookie"
    if original_state != state:
        response.status_code = 400
        return "Invalid state"
    response.delete_cookie("original_state")
    token = oauth2_client.fetch_token(code, state)
    response.set_cookie(
        "token",
        value=token["access_token"],
        httponly=True,
        samesite="lax",
        secure=secure,
    )
    response.set_cookie(
        "access_token",
        value=token["access_token"],
        httponly=True,
        samesite="lax",
        secure=secure,
    )
    response.set_cookie(
        "id_token",
        value=token["id_token"],
        httponly=True,
        samesite="lax",
        secure=secure,
    )


@app.get("/v1/token")
def v1_token(response: Response, access_token: Annotated[str | None, Cookie()] = None):
    if access_token is None:
        response.status_code = 401
        return "Missing token cookie"
    return token


@app.get("/v1/userinfo")
def v1_userinfo(
    response: Response, access_token: Annotated[str | None, Cookie()] = None
):
    if access_token is None:
        response.status_code = 401
        return "Missing token cookie"
    user_info = oauth2_client.fetch_user_info({"access_token": access_token})
    return user_info
