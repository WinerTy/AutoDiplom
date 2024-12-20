from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, AutoPartViewSet, TypesViewSet, AutoMarkView
from api.views.order.order_view import OrderViewSet


def get_router():
    router = DefaultRouter()
    router.register("category", CategoryViewSet)
    router.register("auto/part", AutoPartViewSet)
    router.register("types", TypesViewSet)
    router.register("auto/mark", AutoMarkView)
    router.register("order", OrderViewSet)
    return router


router = get_router()
