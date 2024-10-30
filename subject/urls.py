from django.urls import path
from . import views

urlpatterns = [
    path("toggle_fix/", views.toggle_fix, name="toggle_fix"),
    # 다른 URL 패턴들...
]
