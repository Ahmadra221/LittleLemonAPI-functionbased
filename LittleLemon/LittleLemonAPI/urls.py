from django.urls import path, include
from . import views

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema_view = swagger_get_schema_view(
    openapi.Info(
        title='Little lemon API',
        default_version='1.0.0',
        description='API documentation of App'
    ),
    public= True,
)

urlpatterns = [

    path('menu-items', views.menuitems_api),
    path('menu-items/<int:pk>', views.menu_item),
    path('groups/manager/users', views.product_managers),
    path('groups/manager/users/<int:pk>', views.product_managers_remove),
    path('groups/delivery-crew/users', views.delivery_crew),
    path('groups/delivery-crew/users/<int:pk>', views.delivery_crew_remove),
    path('cart/menu-items', views.cart),
    path('orders', views.order_view),
    path('orders/<int:pk>', views.single_order_view),

    path(
    'swagger/', include([
        path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),

    ])
    ),

    
]
