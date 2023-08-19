from re import compile, IGNORECASE, Pattern
import country_converter as coco


def get_country_regex(country: str) -> Pattern:
    pat = coco.convert(names=country, to="regex", not_found=None)
    if not pat:
        raise ValueError("Unknown country: {}".format(country))

    return compile(pat, IGNORECASE)


def get_country_iso2(country: str) -> str:

    if cn := coco.convert(names=country, to="ISO2", not_found=None):
        return cn
    raise ValueError("Unknown country: {}".format(country))
