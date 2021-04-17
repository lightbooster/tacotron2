import re

_comma_number_re = re.compile(r'([0-9][0-9\,]+[0-9])')
_decimal_number_re = re.compile(r'([0-9]+\.[0-9]+)')
_number_re = re.compile(r'[0-9]+')

ones = (
    u'ноль',

    (u'один', u'одна'),
    (u'два', u'две'),

    u'три', u'четыре', u'пять',
    u'шесть', u'семь', u'восемь', u'девять'
)

teens = (
    u'десять', u'одиннадцать',
    u'двенадцать', u'тринадцать',
    u'четырнадцать', u'пятнадцать',
    u'шестнадцать', u'семнадцать',
    u'восемнадцать', u'девятнадцать'
)

tens = (
    teens,
    u'двадцать', u'тридцать',
    u'сорок', u'пятьдесят',
    u'шестьдесят', u'семьдесят',
    u'восемьдесят', u'девяносто'
)

hundreds = (
    u'сто', u'двести',
    u'триста', u'четыреста',
    u'пятьсот', u'шестьсот',
    u'семьсот', u'восемьсот',
    u'девятьсот'
)

orders = (
    ((u'тысяча', u'тысячи', u'тысяч'), 'f'),
    ((u'миллион', u'миллиона', u'миллионов'), 'm'),
    ((u'миллиард', u'миллиарда', u'миллиардов'), 'm'),
)

decimals = (u'десятых', u'сотых', u'тысячных', u'десятитысячных', u'стотысячных', u'миллионных')

minus = u'минус'


def _thousand(rest, sex):
    prev = 0
    plural = 2
    name = []
    use_teens = rest % 100 >= 10 and rest % 100 <= 19
    if not use_teens:
        data = ((ones, 10), (tens, 100), (hundreds, 1000))
    else:
        data = ((teens, 10), (hundreds, 1000))
    for names, x in data:
        cur = int(((rest - prev) % x) * 10 / x)
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(teens[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                name_ = name_[0 if sex == 'm' else 1]
            name.append(name_)
            if cur >= 2 and cur <= 4:
                plural = 1
            elif cur == 1:
                plural = 0
            else:
                plural = 2
        else:
            name.append(names[cur - 1])
    return plural, name


def _num2text(num, main_units=((u'', u'', u''), 'm')):
    _orders = (main_units,) + orders
    if num == 0:
        return ' '.join((ones[0], _orders[0][0][2])).strip()

    rest = abs(num)
    ord = 0
    name = []
    while rest > 0:
        plural, nme = _thousand(rest % 1000, _orders[ord][1])
        if nme or ord == 0:
            name.append(_orders[ord][0][plural])
        name += nme
        rest = int(rest / 1000)
        ord += 1
    if num < 0:
        name.append(minus)
    name.reverse()
    return ' '.join(name).strip()


def _remove_commas(m):
    return m.group(1).replace(',', '')


def _expand_decimal_point(m):
    decimal_number_str = str(m.group(1))
    point_index = decimal_number_str.find('.')
    full_part = decimal_number_str[:point_index]
    decimal_part = decimal_number_str[point_index + 1:]
    decimal_postfix_index = len(decimal_part) - 1
    decimal_postfix = decimals[decimal_postfix_index if decimal_postfix_index < len(decimals) else ""]
    return f"{_num2text(int(full_part))} целых {_num2text(int(decimal_part))} {decimal_postfix}"


def _expand_number(m):
    num = int(m.group(0))
    return _num2text(num)


def normalize_numbers_ru(text):
    text = re.sub(_comma_number_re, _remove_commas, text)
    text = re.sub(_decimal_number_re, _expand_decimal_point, text)
    text = re.sub(_number_re, _expand_number, text)
    return text


