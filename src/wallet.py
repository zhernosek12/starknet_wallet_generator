from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.hash.address import compute_address

from src.seed_phrase_helper.crypto import HDPrivateKey, HDKey
from src.utils import grid_key, wallet_to_hex, get_wallet_info


class Wallet:
    def __init__(self):
        self.master_key, self.seed_phrase = HDPrivateKey.master_key_from_entropy()
        self.private_key = self.get_argent_private_key(self.seed_phrase)
        self.address = self.calculate_address(self.private_key)

    @staticmethod
    def get_argent_private_key(seed_phrase):
        master_key = HDPrivateKey.master_key_from_mnemonic(seed_phrase)
        root_keys = HDKey.from_path(master_key, "m/44'/60'/0'")
        acct_priv_key = root_keys[-1]
        keys = HDKey.from_path(acct_priv_key, '0/0')
        eth_key = keys[-1]._key.to_hex()

        master_key = HDPrivateKey.master_key_from_seed(eth_key)
        root_keys = HDKey.from_path(master_key, "m/44'/9004'/0'/0/0")
        private_key = grid_key(root_keys[-1]._key.to_hex())

        return private_key

    @staticmethod
    def calculate_address(private_key):
        private_key = int(private_key, 16)
        key_pair = KeyPair.from_private_key(private_key)

        implementation_class_hash, proxy_class_hash, selector, calldata = get_wallet_info(
            key_pair=key_pair
        )

        address = compute_address(
            class_hash=int(implementation_class_hash, 16),
            constructor_calldata=[*calldata],
            salt=key_pair.public_key
        )

        address_hex = wallet_to_hex(address)
        return address_hex
