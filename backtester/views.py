from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from builder.meta import Meta

class BackView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        M = Meta()
        
        return render(request, './templates/backtest.html')