#!/usr/bin/env python3

dict = {
    0: "〇",
    1: "一",
    2: "二",
    3: "三",
    4: "四",
    5: "五",
    6: "六",
    7: "七",
    8: "八",
    9: "九",
    10: "十",
    100: "百",
    1000: "千",
    10000: "万",
    100000: "十万",
    1000000: "百万",
    10000000: "千万",
    100000000: "亿"
}

# DO NOT USE
# Perform the translation recursivly
def replace(number, power):
    if number < 0 or 999999999 < number:
        return str(number)
    if power == 0 and number < 10:
        return dict[number]
    elif power == 0:
        return replace(int((number - (number % 10)) / 10), 10) + dict[number % 10]
    elif number < 10:
        return dict[number] + dict[power]
    else:
        return replace(int((number - (number % 10)) / 10), power * 10) + dict[number % 10] + dict[power]

# Translate a number in chinese
# The number must be between 0 and 999999999 unless it can't be translated
# Return the translated number as a string
# If the number can't be translated, it's returned as a string
def translate(number : int):
    return replace(number, 0)