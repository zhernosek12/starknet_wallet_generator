import csv
import random
import time

from datetime import datetime
from pathlib import Path
from tqdm import tqdm
from loguru import logger

from src.wallet import Wallet
from src.utils import print_logo
from src.config import config


class WalletGenerator:
    @staticmethod
    def generate_wallet() -> Wallet:
        return Wallet()


def main():
    print_logo()

    wallets_rows = []
    filename = f"argent_{len(wallets_rows)}_{str(datetime.now()).replace(' ', '_').replace(':', '.')}.csv"

    root_path = Path(__file__).resolve().parent.parent
    accounts_path = root_path / filename

    for _ in tqdm(range(int(config.wallets_count)), desc='Создаем кошельки: ', unit=' кошельков', colour='GREEN'):
        wallet = WalletGenerator.generate_wallet()
        wallets_rows.append([wallet.address, wallet.private_key, wallet.seed_phrase])
        time.sleep(random.randint(3, 7))

    with open(accounts_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['address', 'private_key', 'seed'])
        writer.writerows(wallets_rows)

    logger.success(f'Argent кошельки успешно созданы. Файл - {filename}')
