def merge_dicts(a: dict, b: dict):
    c = a.copy()
    for key in b:
        if key in c:
            c[key] += b[key]
        else:
            c[key] = b[key]
    return c
