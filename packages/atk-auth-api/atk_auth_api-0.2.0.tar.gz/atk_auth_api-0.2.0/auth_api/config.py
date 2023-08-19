from functools import cache
import logging
import yaml

from pydantic import BaseModel
import requests


class ApiConfig(BaseModel):
    url: str
    allowed_origins: list[str]


class OIDCConfig(BaseModel):
    url: str
    client_id: str
    client_secret: str


class Config(BaseModel):
    api: ApiConfig
    oidc: OIDCConfig


def read_config_file(path: str) -> Config:
    with open(path) as f:
        return Config(**yaml.safe_load(f))


class DexConfig(BaseModel):
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    userinfo_endpoint: str
    jwks_uri: str


@cache
def fetch_openid_config(url: str) -> DexConfig:
    well_known_url = url.rstrip("/") + "/.well-known/openid-configuration"
    wanted_fiends = [field for field in DexConfig.__fields__]
    logging.info("Fetching OpenID config from %s", well_known_url)
    response = requests.get(well_known_url)
    response.raise_for_status()
    response_dict = response.json()
    return DexConfig(**{k: response_dict[k] for k in wanted_fiends})
