from pathlib import Path

from email_attachment_downloader.google_utils import build_api
from email_attachment_downloader.utils import download_message_attachment
from email_attachment_downloader.config import Config


def main(config_path: Path):
    config = Config.parse_from_toml(config_path)
    Path(config.attachment_download_dir).mkdir(parents=True, exist_ok=True)

    user_id = 'me'
    service = build_api(config.google_credentials_path, config.google_token_path)

    result = service.users().messages().list(userId=user_id, q=f'from:{config.sender_email_address}').execute()
    messages = result['messages']

    for message in messages:
        full_message = service.users().messages().get(userId=user_id, id=message['id']).execute()
        download_message_attachment(service,
                                    full_message,
                                    user_id,
                                    config.attachment_download_dir,
                                    config.attachment_extension)


if __name__ == '__main__':
    main(Path('./config.toml'))
