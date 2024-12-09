from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, AutoPartViewSet, TypesViewSet


def get_router():
    router = DefaultRouter()
    router.register("category", CategoryViewSet)
    router.register("auto.part", AutoPartViewSet)
    router.register("types", TypesViewSet)
    return router


router = get_router()
