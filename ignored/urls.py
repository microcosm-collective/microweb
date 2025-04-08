from django.conf.urls import url

from ignored import views

urlpatterns = [
    url(r"^ignored/$", views.ignored, name="list-ignored"),
    url(r"^ignore/$", views.ignore, name="ignore-item"),
    url(r"^unignore/$", views.ignore, name="unignore-item"),
]
