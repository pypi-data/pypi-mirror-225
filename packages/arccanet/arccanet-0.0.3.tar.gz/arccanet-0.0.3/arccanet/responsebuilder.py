import datetime
import math
from .general import safe_division


def paginate(resp, pagination, total):
    return {
        'total_pages': math.ceil(total / pagination['size']),
        'results': resp
    }


def populate_by_month(query_response, first_date, date_index=0, default=0, keys=["rev"]):
    resp = []
    it = first_date
    current_month = first_date.month
    aux_it = 0
    n_keys = len(keys)
    while it.month == current_month:
        if aux_it < len(query_response) and it == query_response[aux_it][date_index]:
            r = {'date': it}
            for i in range(n_keys):
                r[keys[i]] = query_response[aux_it][1 + i]
            resp.append(r)
            aux_it += 1
        else:
            r = {'date': it}
            for i in range(n_keys):
                r[keys[i]] = default
            resp.append(r)
        it = it + datetime.timedelta(days=1)
    return resp


def populate_by_aggregation(query_response, first_date, final_date, agg, date_index=0, default=0, keys=["rev"]):
    resp = []
    it = first_date
    aux_it = 0
    n_keys = len(keys)
    while 1:
        if aux_it < len(query_response) and agg.datetime_to_string(it) == query_response[aux_it][date_index]:
            r = {'date': it}
            for i in range(n_keys):
                r[keys[i]] = query_response[aux_it][1 + i]
            resp.append(r)
            aux_it += 1
        else:
            r = {'date': it}
            for i in range(n_keys):
                r[keys[i]] = default
            resp.append(r)
        it = agg.get_next(it)
        if it > final_date:
            return resp


def obj_list(query, fields):
    n = len(fields)
    resp = []
    for line in query:
        r = {}
        for i in range(n):
            r[fields[i]] = line[i]
        resp.append(r)
    return resp


def obj(query, fields):
    r = {}
    for i in range(len(fields)):
        r[fields[i]] = query[i]
    return r


def obj_from_lines(query, index=1):
    r = {}
    for line in query:
        r[line[0]] = line[index]
    return r


def obj_from_lines_division(query):
    r = {}
    for line in query:
        r[line[0]] = safe_division(line[1], line[2])
    return r


def sum_index(query, index):
    s = 0
    for line in query:
        s += line[index]
    return s


def populate_array_by_dates(query, initial_date, final_date):
    i = 0
    resp = []
    it = initial_date
    while it <= final_date:
        percentage = 0
        if i < len(query) and query[i][0] == it:
            percentage = query[i][1]
            i += 1
        resp.append(percentage)
        it = it + datetime.timedelta(days=1)
    return resp


def populate_and_group_by_dates(query, initial_date, final_date, date_index=0, group_index=1, value_index=2):
    n = len(query)
    resp = []
    it = initial_date
    aux = 0
    while 1:
        aux_obj = {'date': it}
        while aux < n and it == query[aux][date_index]:
            aux_obj[query[aux][group_index]] = query[aux][value_index]
            aux += 1
        resp.append(aux_obj)
        if it == final_date:
            break
        it = it + datetime.timedelta(days=1)
    return resp


def group_by(query, field):
    resp = []
    n = len(query)
    it = 0
    while it < n:
        aux_obj = {field: query[it][0]}
        while it < n and query[it][0] == aux_obj[field]:
            aux_obj[query[it][1]] = query[it][2]
            it += 1
        resp.append(aux_obj)
    return resp
