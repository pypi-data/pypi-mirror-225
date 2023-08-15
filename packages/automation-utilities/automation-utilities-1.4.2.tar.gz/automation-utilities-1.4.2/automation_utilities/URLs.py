from urllib.parse import urlparse, parse_qs, unquote


def get_parameters(url: str) -> dict:
    dictionary = parse_qs(urlparse(unquote(url)).query)
    return {key: dictionary[key][0] if len(dictionary[key]) == 1 else dictionary[key] for key in dictionary.keys()}
