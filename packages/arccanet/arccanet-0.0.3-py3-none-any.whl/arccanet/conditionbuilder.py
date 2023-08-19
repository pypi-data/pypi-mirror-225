def multiple(field, arr):
    if len(arr) == 0:
        return field + ' in (null)'
    cond = ''
    for el in arr:
        cond += str(el) + ','
    return field + ' in (' + cond[:-1] + ')'


def single(field, val, prepend=''):
    if val is None:
        return ''
    return prepend + field + ' = ' + str(val)


def profile_group(p, exclude_holding=True, prepend=''):
    if p is None:
        return prepend + "h.value != 0" if exclude_holding else ''
    if p.hierarchy.value == 0 and exclude_holding:
        return prepend + "false"
    return prepend + "pg.id = " + str(p.id)


def uc_status(uc, prepend=''):
    if uc == '' or uc is None:
        return ""
    if uc == 'Y':
        return prepend + "uc_status = 'Y'"
    return prepend + "uc_status = 'N' or uc_status is null"


def is_target(it, prepend=''):
    if it is None:
        return ""
    if it:
        return prepend + "ctg.id is not null"
    return prepend + "ctg.id is null"


def fuzzy(string, field, limit, with_condition=True, prepend='', append=''):
    if string == "":
        return ""
    if limit is None:
        filter_text = f"levenshtein(lower({field}), '{string.lower()}')"
    else:
        filter_text = f"levenshtein_less_equal(lower({field}), '{string.lower()}', 1, 0, 1, {limit})"
    if with_condition and limit is not None:
        filter_text += f" <= {limit}"
    return prepend + filter_text + append
