__author__ = 'TianShuo'

import os
import os.path

from os import environ

is_sae = environ.get("APP_NAME", "")
if is_sae:
    import sae.kvdb

    kv = sae.kvdb.KVClient()
else:
    pass
    #exit()


def check_cache(hash):
    if is_sae:
        if hash == 'none':
            return False
        else:
            return get_cache(hash)


def get_cache(hash):
    if is_sae:
        if not kv.get(hash):
            return False
        else:
            return kv.get(hash)

def set_cache(hash, content):
    if is_sae:
        if not kv.get(hash):
            return kv.add(hash, content)
        else:
            return kv.set(hash, content)


def clear_cache(hash):
    if is_sae:
        pass
