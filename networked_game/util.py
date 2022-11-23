def merge_dicts(a: dict, b: dict):
    c = a.copy()
    for key in b:
        if key in c:
            c[key] += b[key]
        else:
            c[key] = b[key]
    return c


def format_resources(resources, skip_blanks):
    points = resources['points'] if 'points' in resources else 0
    black = resources['black'] if 'black' in resources else 0
    orange = resources['orange'] if 'orange' in resources else 0
    purple = resources['purple'] if 'purple' in resources else 0
    white = resources['white'] if 'white' in resources else 0
    coins = resources['coins'] if 'coins' in resources else 0
    result = ""

    if points or not skip_blanks:
        result += f"Points: {points:3} -"
    if black or not skip_blanks:
        result += f" {black:2}B"
    if orange or not skip_blanks:
        result += f" {orange:2}O"
    if purple or not skip_blanks:
        result += f" {purple:2}P"
    if white or not skip_blanks:
        result += f" {white:2}W"
    if coins or not skip_blanks:
        result += f" {coins:2}C"

    return result
