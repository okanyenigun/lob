from django.urls import path
from builder.views import BuilderView

urlpatterns = [
    path('', BuilderView.as_view(), name="builder"),
]
