from django.urls import path
from builder.views import BuilderView, HomeView

urlpatterns = [
    path('', BuilderView.as_view(), name="builder"),
    path('home/', HomeView.as_view(), name="home"),
]
