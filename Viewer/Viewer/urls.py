"""
URL configuration for Viewer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from waters.views import home, new_run, post_run, show, refresh, \
    add_checkbox, add_istd_box, save_istd, save_check, \
    export_method, import_method

urlpatterns = [
    path('', home),
    path('new_run', new_run),
    path('post_run', post_run),
    path('admin/', admin.site.urls),
    path('show/<int:run_id>', show),
    path('refresh', refresh),
    path('checkboxes', add_checkbox),
    path('istd_box', add_istd_box),
    path('save_istd', save_istd),
    path('save_check', save_check),
    path('export_method/<int:run_id>', export_method),
    path('import_method/<int:run_id>', import_method),
]
