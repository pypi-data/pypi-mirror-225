from typing import Tuple


def validate_context_kv_pair(kv_pair: str) -> Tuple[str, str]:
    kv_pair = kv_pair.strip()
    assert '=' in kv_pair, f'{kv_pair} does not follow the syntax key=kv_pairue pair.'
    parts = kv_pair.split('=')
    if len(parts) > 2:
        raise ValueError(f'{kv_pair} does not follow the syntax key=kv_pairue pair.')
    key, val = parts
    return key, val
