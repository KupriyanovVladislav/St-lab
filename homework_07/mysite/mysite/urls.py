"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include

from main import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:shop_id>/', views.ShopView.as_view(), name='shop'),
    path('<int:shop_id>/<int:department_id>/addItem', views.ItemCreate.as_view()),
    path('<int:shop_id>/<int:department_id>/<int:item_id>/deleteItem', views.ItemDelete.as_view()),
    path('<int:shop_id>/<int:department_id>/<int:item_id>/updateItem', views.ItemUpdate.as_view(), name='item_update'),
    path('<int:shop_id>/addDepartment', views.DepartmentCreate.as_view()),
    path('<int:shop_id>/<int:department_id>/deleteDepartment', views.DepartmentDelete.as_view()),
    path('<int:shop_id>/<int:department_id>/updateDepartment', views.DepartmentUpdate.as_view()),
    path('filter/item/<int:number>/', views.FilteredItemsView.as_view()),
    path('filter/shop/<int:number>/', views.FilteredShopsView.as_view()),
    path('<int:shop_id>/infoShop/', views.ShopInfoView.as_view()),
    path('<int:shop_id>/infoShop/deleteShop/', views.ShopDelete.as_view()),
    path('<int:shop_id>/infoShop/updateShop/', views.ShopUpdate.as_view()),
    path('compare/departments/', views.ComparedDepartmentsView.as_view()),
    path('disabled/', views.DisabledView.as_view(), name='disabled'),
]
