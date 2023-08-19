from datetime import datetime
from datetime import timedelta
from typing import Union
from sqlite3 import OperationalError
from hashlib import md5
from base64 import b64decode, b64encode
from .config import Config
from .db import *
from .spreadsheet_parsing import get_book, parse_platform_models, platforms
from .countries import get_country_iso2


class CiscoAPLookup:

    @classmethod
    def models(cls) -> list[str]:
        return get_models()

    @classmethod
    def domain_for(cls, model: str, cn_iso2: str = None) -> list[str]:
        """
        Get list of possible regulatory domains for AP model and optionally country
        :param str model: AP Model name (without regulatory domain part)
        :param str cn_iso2: iso2 country - detects iso2 from full name, but with perf. impact.
        :rtype: list[str]
        """
        if cn_iso2 and len(cn_iso2) > 2:
            cn_iso2 = get_country_iso2(cn_iso2)
        return get_domain_for(model, cn_iso2)

    @classmethod
    def models_for(cls, model: str, cn_iso2: str = None) -> list[str]:
        """
        Get list of AP model PIDs with RD for model and optionally country
        :param str model: AP Model name (without regulatory domain part)
        :param str cn_iso2: iso2 country - detects iso2 from full name, but with perf. impact.
        :rtype: list[str]
        """
        if cn_iso2 and len(cn_iso2) > 2:
            cn_iso2 = get_country_iso2(cn_iso2)
        return get_models_for(model, cn_iso2)

    @classmethod
    def country_models(cls, model: str) -> list[str]:
        """
        Get list of unique AP model PIDs with RD for model
        :param str model: AP Model name (without regulatory domain part)
        :rtype: list[str]
        """
        return get_models_for(model)


def _refresh_required() -> Union[bool, bytearray]:
    hash_ = None
    try:
        hash_, date = get_file_hash(Config.CISCO_XLS_URL)
        if date:
            date = datetime.fromtimestamp(date)
            if date + timedelta(days=Config.REFRESH_DAYS) > datetime.now():
                return False  # refresh not passed yet

    except StopIteration as e:
        pass
    import requests
    xls_data = requests.get(Config.CISCO_XLS_URL, allow_redirects=True).content
    if hash_ and hash_ == b64encode(md5(xls_data).digest()).decode("utf-8"):
        return False  # no change in file
    return xls_data


def _refresh_data(xls_data: bytearray):
    from io import BytesIO
    new_md5 = b64encode(md5(xls_data).digest()).decode("utf-8")
    wb = get_book(BytesIO(xls_data))
    prune = True
    init_db()
    for platform in platforms:
        models = parse_platform_models(wb, platform)
        insert_models(models, prune)
        prune = False
    update_file_hash(Config.CISCO_XLS_URL, new_md5)


if new_data := _refresh_required():
    _refresh_data(new_data)


__all__ = ["CiscoAPLookup"]
