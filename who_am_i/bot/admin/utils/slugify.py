def build_slug(text: str) -> str:
    translit_map = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ё': 'e',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'й': 'y',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'h',
        'ц': 'ts',
        'ч': 'ch',
        'ш': 'sh',
        'щ': 'sch',
        'ъ': '',
        'ы': 'y',
        'ь': '',
        'э': 'e',
        'ю': 'yu',
        'я': 'ya',
    }

    text = text.lower()
    title = '-'.join(text.split())

    result = []
    for sym in title:
        if sym in translit_map:
            result.append(translit_map[sym])
        elif sym == '-':
            result.append(sym)
        elif 'a' <= sym <= 'z' or sym.isdigit():
            result.append(sym)
        else:
            continue

    slug = ''.join(result)
    while '--' in slug:
        slug = slug.replace('--', '-')

    slug = slug.strip('-')
    if not slug:
        slug = 'quiz-slug'

    return slug
