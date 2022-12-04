from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from builder.service.proc import DataBuilder
from builder.meta import Meta

class BuilderView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        if "submit-build" in request.GET:
            M = Meta()
            M.df_lob = DataBuilder.build(M.path)
            return redirect("backtester")
        return render(request, './templates/builder.html')