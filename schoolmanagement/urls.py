from django.contrib import admin
from django.urls import path,include
from school import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('', include('school.urls'))
    ]


    