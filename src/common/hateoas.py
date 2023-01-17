from typing import List, Dict
from flask import url_for

def pagination_links(items: List, page: int, per_page: int, endpoint: str) -> Dict:
    
    links = {
        "first": url_for(endpoint, page=1, per_page=per_page, _external=True),
        "prev": url_for(endpoint, page=page-1, per_page=per_page, _external=True) if page > 1 else None,
        "self": url_for(endpoint, page=page, per_page=per_page, _external=True),
        "next": url_for(endpoint, page=page+1, per_page=per_page, _external=True),
        "last": url_for(endpoint, page=items.pages, per_page=per_page, _external=True)
    }

    return {
        "items": [item.json(links=True) for item in items.items],
        "pagination": {
            "count": items.total,
            "page": page,
            "per_page": per_page,
            "pages": items.pages,
            "links": links
        }
    }