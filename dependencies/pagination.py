def get_pagination(page:int | None = None, limit:int | None = None):
    return {
        "page" : page,
        "limit" : limit
    }
