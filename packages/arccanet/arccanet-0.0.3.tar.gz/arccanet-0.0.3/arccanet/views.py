from rest_framework.views import APIView as View
from django.db import connection


class APIView(View):
    cursor = None

    def dispatch(self, request, *args, **kwargs):
        self.cursor = connection.cursor()
        resp = super(APIView, self).dispatch(request, *args, **kwargs)
        self.cursor.close()
        return resp
