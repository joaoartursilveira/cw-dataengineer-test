from collections.abc import MutableMapping
from dataclasses import dataclass


@dataclass
class CountryData:
    """
    Worldbank api json content as a dataclass representation.
    """
    indicator_id: str
    indicator_value: str
    country_id: str
    country_value: str
    countryiso3code: str
    date: int
    value: float
    unit: str
    obs_status: str
    decimal: int


def _flatten_dict_gen(d, parent_key, sep):
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            yield from flatten_dict(v, new_key, sep=sep).items()
        else:
            yield new_key, v


def flatten_dict(d: MutableMapping, parent_key: str = '', sep: str = '.') -> dict:
    """
    Flats nested dictionaries based on given separator, being . the default.
    """
    return dict(_flatten_dict_gen(d, parent_key, sep))
