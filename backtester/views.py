from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from backtester.controller import BackController
from builder.meta import Meta
from utility.utils import Utility

class BackView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, './templates/backtest.html')

    def post(self, request: HttpRequest):
        params, percents = BackController.parse_input(request)
        print("params: ",params)
        print("percents: ",percents)
        BackController.run_backtest(params, percents)
        return render(request, './templates/backtest.html')