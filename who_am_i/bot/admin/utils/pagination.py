from typing import TypeVar


T = TypeVar('T')


async def pagination_of_buttons(
    items: list[T],
    page: int,
) -> tuple[bool, bool, list[T]]:
    page_size = 5
    start = page * page_size
    end = start + page_size
    page_items = items[start:end]

    has_prev = page > 0
    has_next = end < len(items)

    return has_prev, has_next, page_items
