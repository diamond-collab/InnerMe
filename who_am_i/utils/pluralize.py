def pluralize(number: int, forms: tuple[str, str, str]) -> str:
    last_two_digits = number % 100
    if 11 <= last_two_digits <= 14:
        return forms[2]

    last_digit = number % 10
    if last_digit == 1:
        return forms[0]

    if last_digit in (2, 3, 4):
        return forms[1]

    return forms[2]
