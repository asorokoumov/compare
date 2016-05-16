def item_url(url, seller):
    if seller.name == "Korablik":
        return url.split('?')[0]
    else:
        return url
