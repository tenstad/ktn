from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View


def try_next(request, default):
    try:
        return HttpResponseRedirect(request.GET['next'])
    except KeyError:
        return HttpResponseRedirect(default)


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'ktn/index.html')
