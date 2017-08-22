import json
from copy import deepcopy
from functools import wraps

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static

WEBPACK_ASSETS_DIR = settings.WEBPACK_ASSETS_DIR
_RESULT_CACHE = {}


def _cache(f):
    cache_key = id(f)

    @wraps(f)
    def wrapper(*args, **kwargs):
        if cache_key not in _RESULT_CACHE or settings.DEBUG:
            _RESULT_CACHE[cache_key] = f(*args, **kwargs)
        return _RESULT_CACHE[cache_key]

    return wrapper


def _load_assets_json():
    assets_path = WEBPACK_ASSETS_DIR.joinpath('webpack-assets.json')
    return json.loads(open(assets_path, 'rt').read())


def _read_bootstrap(assets_json):
    bootstrap_path = WEBPACK_ASSETS_DIR.joinpath(assets_json['bootstrap']['js'])
    return open(bootstrap_path, 'rt').read()


def _transform_webpack_assets(assets_json):
    assets_json = deepcopy(assets_json)
    for _, chunk in assets_json.items():
        for asset_kind, value in chunk.items():
            chunk[asset_kind] = static(value)
    return assets_json


@_cache
def assets():
    assets_json = _load_assets_json()
    return _transform_webpack_assets(assets_json)


@_cache
def bootstrap():
    assets_json = _load_assets_json()
    return _read_bootstrap(assets_json)


__all__ = ['assets', 'bootstrap']
