from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from backtester.controller import BackController


class BackView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, './templates/backtest.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        context= {}
        #get bucket input
        params, percents = BackController.parse_input(request)
        #testing
        context["transaction"], context["buy_orders"], context["sell_orders"], context["profit"] = BackController.run_backtest(params, percents)
        return render(request, './templates/backtest.html', context)