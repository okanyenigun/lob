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
            M = Meta()
            M.df_lob = DataBuilder.build(M.path)
            #M.df_lob = pd.read_excel("D:\\Documents\\Desktop\\akb\\lob.xlsx")
            return redirect("home")
        return render(request, './templates/builder.html')

class HomeView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {"indicator": "macd"}
        M = Meta()
        if "get_excel" in request.GET:
            path = BuilderController.create_excel_for_df()
            file = Utility.download_static_file(path)
            if file:
                return file
        if "indicator" in request.GET:
            context["indicator"] = request.GET.get("indicator")
        context = BuilderController.collect_page_elements(M.df_lob, context["indicator"])
        return render(request, './templates/home.html', context)