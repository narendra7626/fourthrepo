"""ecommercepractie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url,include
from myapp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.home,name='home'),
    url(r'^category/$',views.CategoryView.as_view(),name='category'),
    path('category_product_list/<slug:slug>/',views.CategoryProductList.as_view(),name='category_product_list'),
    path('product_detail/<slug:slug>/',views.ProductDetail.as_view(),name='product_detail'),
    path('cart_add/<int:pro_id>/',views.Cart_Add.as_view(),name='cart_add'),
    path('mycart/',views.mycart,name='mycart'),
    path('managecart/<int:cp_id>/',views.ManageCartView.as_view(),name='managecart'),
    path('emptycart/',views.EmptyCartView.as_view(),name="emptycart"),
    path('checkout/',views.CheckOutView.as_view(),name='checkout'),
    url(r'^search/$',views.search,name='search'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
