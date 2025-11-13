from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout/password
    path('', RedirectView.as_view(pattern_name='groups:list', permanent=False)),
    path('groups/', include('groups.urls')),
]
