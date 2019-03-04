import logging
logger = logging.getLogger('compare')


def item_url(url, seller):
    if seller.name == "Korablik":
        return url.split('?')[0]
    else:
        return url


def next_url(url, seller):
    if seller.name == "Akusherstvo" and url:
        url = url.split('akusherstvo.ru')
        return url[-1:]
    else:
        return url


def decode_url(url):
    url = url.replace('+', 'plus')
    url = url.replace('/', '--')
    return url


def encode_url(url):
    url = url.replace('plus', '+')
    url = url.replace('--', '/')
    return url
