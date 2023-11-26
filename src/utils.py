import hashlib
from starknet_py.hash.selector import get_selector_from_name


def get_wallet_info(key_pair):
    implementation_class_hash = '0x1a736d6ed154502257f02b1ccdf4d9d1089f80811cd6acad48e6b6a9d1f2003'
    proxy_class_hash = int('0x025ec026985a3bf9d0cc1fe17326b245dfdc3ff89b8fde106542a3ea56c5a918', 16)
    selector = get_selector_from_name('initializer')
    calldata = [key_pair.public_key, 0]
    return implementation_class_hash, proxy_class_hash, selector, calldata


def wallet_to_hex(value: int):
    if isinstance(value, int):
        return '0x{:064x}'.format(value)


def concat(a, b):
    return a + b


def arrayify(hex_string_or_big_number_or_arrayish):
    try:
        value = int(hex_string_or_big_number_or_arrayish)
    except ValueError:
        value = int(hex_string_or_big_number_or_arrayish, 16)

    if value == 0:
        return [0]

    hex_v = hex(value)[2:]

    if len(hex_v) % 2 != 0:
        hex_v = "0" + hex_v

    result = []
    for i in range(len(hex_v) // 2):
        offset = i * 2
        result.append(int(hex_v[offset:offset + 2], 16))

    return result


def hash_key_with_index(key, index):
    payload = concat(arrayify(key), arrayify(index))
    payload_hash = get_payload_hash(payload)
    return int(payload_hash, 16)


def grid_key(key_seed):
    KEY_VALUE_LIMIT = 0x800000000000010ffffffffffffffffb781126dcae7b2321e66a241adc64d2f
    SHA256_EC_MAX_DIGEST = 0x10000000000000000000000000000000000000000000000000000000000000000

    max_allowed_val = SHA256_EC_MAX_DIGEST - (SHA256_EC_MAX_DIGEST % KEY_VALUE_LIMIT)
    i = 0
    key = 0

    while True:
        key = hash_key_with_index(key_seed, i)
        i += 1
        if key <= max_allowed_val:
            break

    res = hex(abs(key % KEY_VALUE_LIMIT))
    return res


def get_payload_hash(payload):
    m = hashlib.sha256()

    for value in payload:
        hex_value = hex(value)[2::]
        if len(hex_value) == 1:
            hex_value = "0" + hex_value
        m.update(bytes.fromhex(hex_value))

    return m.hexdigest()


def print_logo():
    logo = '''
    ______  _____  _____   ___   _____   __   __   _____ ______ __   ________  _____  _   _  _____ 
    | ___ \|  ___||  __ \ / _ \ /  ___|  \ \ / /  /  __ \| ___ \\\ \ / /| ___ \|_   _|| | | |/  ___|
    | |_/ /| |__  | |  \// /_\ \\\ `--.    \ V /   | /  \/| |_/ / \ V / | |_/ /  | |  | | | |\ `--. 
    |  __/ |  __| | | __ |  _  | `--. \   /   \   | |    |    /   \ /  |  __/   | |  | | | | `--. \\
    | |    | |___ | |_\ \| | | |/\__/ /  / /^\ \  | \__/\| |\ \   | |  | |      | |  | |_| |/\__/ /
    \_|    \____/  \____/\_| |_/\____/   \/   \/   \____/\_| \_|  \_/  \_|      \_/   \___/ \____/ 

    '''
    print(logo)