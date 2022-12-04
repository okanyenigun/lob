from django.urls import path
from backtester.views import BackView

urlpatterns = [
    path('backtester/', BackView.as_view(), name="backtester"),
]
