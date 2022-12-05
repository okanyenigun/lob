from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from backtester.controller import BackController
from builder.meta import Meta
from utility.utils import Utility

class BackView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        M = Meta()
        if "get_excel" in request.GET:
            path = BackController.create_excel_for_df()
            file = Utility.download_static_file(path)
            if file:
                return file
        if "indicator_chart" in request.GET:
            indicator = request.GET.get("indicator")
        context = BackController.collect_page_elements(M.df_lob, indicator)
        return render(request, './templates/backtest.html', context)