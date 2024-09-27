from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import tomllib

from dotenv import load_dotenv


@dataclass
class Config:
    google_credentials_path: str
    google_token_path: str
    sender_email_address: str
    attachment_download_dir: str
    attachment_extension: str
    unlocked_save_dir: str

    @staticmethod
    def parse_from_toml(filename: Path) -> Config:
        with open(filename, "rb") as f:
            data = tomllib.load(f)
        return Config(
            google_credentials_path=data['google_credentials_path'],
            google_token_path=data['google_token_path'],
            sender_email_address=data['sender_email_address'],
            attachment_download_dir=data['attachment_download_dir'],
            attachment_extension=data['attachment_extension'],
            unlocked_save_dir=data['unlocked_save_dir']
        )


@dataclass
class Secrets:
    attachment_password: str

    @staticmethod
    def load_from_env():
        if 'ATTACHMENT_PASSWORD' not in os.environ:
            load_dotenv()
        return Secrets(attachment_password=os.environ['ATTACHMENT_PASSWORD'])
