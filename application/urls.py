from django.contrib import admin
from django.urls import include, re_path, path
from django.shortcuts import render


def react_app(request):
    return render(request, 'index.html')

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/products/', include('products.urls', namespace='products')),
    re_path(r'^api/qrs/', include('qr_codes.urls', namespace='qr_codes')),
    re_path(r"^$", react_app),
    re_path(r"^(?:.*)/?$", react_app),
]
