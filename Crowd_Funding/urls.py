"""
URL configuration for Crowd_Funding project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path ,include
from django.conf.urls.static import static
from django.conf import settings
<<<<<<< HEAD
from projects import views as projects

=======
from django.conf.urls.static import static
>>>>>>> 92933ca6c6bbff07aa1e2222648e1660ecf9d5b2

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
<<<<<<< HEAD
    path('categories/add', projects.add_category),

] +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


=======
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> 92933ca6c6bbff07aa1e2222648e1660ecf9d5b2
