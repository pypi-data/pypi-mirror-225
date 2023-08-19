import copy
import datetime
import json
import os
from django.http import Http404
from .exceptions import ValidationError


def get_infra_env():
    if os.environ.get("ENVIRON") == 'production':
        return 'production'
    return 'staging'


def get_base_lambda_name():
    return "arccanet-infra-{}-".format(get_infra_env())


def parse_json(data):
    try:
        return json.loads(data)
    except Exception:
        raise ValidationError("Invalid JSON: {}".format(data))


def get_store_today(timezone):
    return (datetime.datetime.utcnow() - datetime.timedelta(minutes=timezone)).date()


def to_none(val):
    if val == '':
        return None
    return val


def search_object(model, pk):
    q_set = model.objects.filter(pk=pk)
    if not q_set.exists():
        raise Http404
    return q_set[0]


def search_object_with_soft_delete(model, pk):
    q_set = model.objects.filter(pk=pk, deleted_at=None)
    if not q_set.exists():
        raise Http404
    return q_set[0]


def search_object_custom(model, obj):
    q_set = model.objects.filter(**obj)
    if not q_set.exists():
        return None
    return q_set[0]


def search_model_by_fields(data, fields, model, default_obj={}):
    for field in fields:
        if data.get(field) is not None:
            obj = copy.copy(default_obj)
            obj[field] = data[field]
            customer = search_object_custom(model, obj)
            if customer is not None:
                return customer, field
    return None, None


def get_starting_minutes(as_time=False):
    starting_minutes = 360
    if as_time:
        return datetime.time(starting_minutes // 60, starting_minutes % 60)
    return starting_minutes


def safe_division(a, b, default=None):
    return a / b if b != 0 else default


class AggregationPeriod:
    def __init__(self, agg):
        if agg == "day":
            def get_next(it):
                return it + datetime.timedelta(days=1)

            self.format = "YYYY-MM-DD"
            self.datetime_to_string = str
            self.get_next = get_next
            self.approximate_days = 1
        elif agg == "week":
            def datetime_to_string(week):
                iso = week.isocalendar()
                return str(iso[0]) + "-" + ("0" if iso[1] < 10 else "") + str(iso[1])

            def get_next(it):
                iso = it.isocalendar()
                return datetime.date.fromisocalendar(iso[0], iso[1], 7) + datetime.timedelta(days=1)

            self.format = "IYYY-IW"
            self.datetime_to_string = datetime_to_string
            self.get_next = get_next
            self.approximate_days = 7
        elif agg == "month":
            def datetime_to_string(month):
                return month.strftime('%Y-%m')

            def get_next(it):
                if it.month != 12:
                    return datetime.date(it.year, it.month + 1, 1)
                return datetime.date(it.year + 1, 1, 1)

            self.format = "YYYY-MM"
            self.datetime_to_string = datetime_to_string
            self.get_next = get_next
            self.approximate_days = 30
        elif agg == "year":
            def datetime_to_string(year):
                return year.strftime('%Y')

            def get_next(it):
                return datetime.date(it.year + 1, 1, 1)

            self.format = "YYYY"
            self.datetime_to_string = datetime_to_string
            self.get_next = get_next
            self.approximate_days = 365
