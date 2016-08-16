import logging
logger = logging.getLogger('compare')


def item_url(url, seller):
    if seller.name == "Korablik":
        return url.split('?')[0]
    elif seller.name == "Akusherstvo":
        return '/'+url
    else:
        return url


def next_url(url, seller):
    if seller.name == "Akusherstvo" and url:
        return '/magaz.php' + url
    else:
        return url


def description(text, seller):
    if seller.name == "Akusherstvo":
        return text.encode('latin1').decode('cp1251')
    else:
        return text
