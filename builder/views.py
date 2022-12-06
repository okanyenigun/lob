from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse
from builder.service.proc import DataBuilder
from builder.meta import Meta
from builder.controller import BuilderController
from utility.utils import Utility
import pandas as pd

class BuilderView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        if "submit-build" in request.GET:
            #build data
            M = Meta()
            M.df_lob = DataBuilder.build(M.path)
            return redirect("home")
        return render(request, './templates/builder.html')

class HomeView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        indicator = "macd"
        if "get_excel" in request.GET:
            #download lob excel
            path = BuilderController.create_excel_for_df()
            file = Utility.download_static_file(path)
            if file:
                return file
        if "indicator" in request.GET:
            #update plotly chart
            indicator = request.GET.get("indicator")
        context = BuilderController.collect_page_elements(indicator)
        context["indicator"] = indicator
        return render(request, './templates/home.html', context)