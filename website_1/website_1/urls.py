"""
URL configuration for website_1 project.

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
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static  

from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login, name='home_page'),

    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('find/', views.find_page, name='find_page'),
    path('find/<int:item_id>/', views.find_page, name='find_page'),
    
    path('find2/<int:i>/',views.show,name='show'),
    path('show_map/<int:your_model_id>/',views.show_map, name='show_map'),
    path('log/',views.login,name='login'),
    path('homePager/', views.homePager, name='homePager'),
    path('sort/',views.sort,name='sort'),
    path('search/',views.search,name="search"),
    path('emergency/',views.emg1,name='emg1'),
    path('gohome/',views.home_page,name='hm1'),
    path('login/',views.regter,name='regter'),
    path('locate/',views.locate,name='location'),
    path('download/<int:image_id>/',views.download,name='download'),
    

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)