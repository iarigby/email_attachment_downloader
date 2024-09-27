from email_downloader.config import Config, Secrets
from pathlib import Path
import pikepdf


def main(config_path: Path):
    config = Config.parse_from_toml(config_path)
    secrets = Secrets.load_from_env()
    Path(config.unlocked_save_dir).mkdir(parents=True, exist_ok=True)
    for file in Path(config.attachment_download_dir).glob("*"+config.attachment_extension):
        pdf = pikepdf.open(str(file), password=secrets.attachment_password)
        pdf.save(config.unlocked_save_dir + '/' + file.name)


if __name__ == '__main__':
    main(Path('./config.toml'))
