from functools import lru_cache

from pydantic import BaseSettings


class Config(BaseSettings):
    """
    BaseSettings reads in environment variables and stores them in the variables below.
    """
    app_home: str 
    app_name: str = "PeerIQ-Challenge"
    app_mode: str = "development"
    app_version: str = "0.1.0"


@lru_cache()  # no parenthesis in python3.8
def get_config() -> Config:
    return Config()
