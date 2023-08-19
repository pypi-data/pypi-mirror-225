from typing import Tuple

from requests_oauthlib import OAuth2Session

from .config import OIDCConfig, DexConfig


class OAuth2Client:
    def __init__(
        self,
        oidc_config: OIDCConfig,
        dex_config: DexConfig,
        redirect_uri: str,
    ):
        self.config = oidc_config
        self.dex_config = dex_config
        self.redirect_uri = redirect_uri

    def authorization_url(self, scope: list[str]) -> Tuple[str, str]:
        session = OAuth2Session(
            client_id=self.config.client_id, redirect_uri=self.redirect_uri, scope=scope
        )
        url, state = session.authorization_url(self.dex_config.authorization_endpoint)
        return url, state

    def fetch_token(self, code: str, state: str) -> dict:
        session = OAuth2Session(
            client_id=self.config.client_id,
            redirect_uri=self.redirect_uri,
            state=state,
        )
        token = session.fetch_token(
            token_url=self.dex_config.token_endpoint,
            client_secret=self.config.client_secret,
            code=code,
            state=state,
        )
        return token

    def fetch_user_info(self, token: str) -> dict:
        session = OAuth2Session(
            client_id=self.config.client_id,
            redirect_uri=self.redirect_uri,
            token=token,
        )
        return session.get(self.dex_config.userinfo_endpoint).json()
