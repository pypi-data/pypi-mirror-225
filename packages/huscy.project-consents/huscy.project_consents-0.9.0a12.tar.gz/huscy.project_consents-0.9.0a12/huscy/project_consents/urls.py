from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views, viewsets
from huscy.projects.api_urls import project_router


router = DefaultRouter()
router.register(
    'projectconsentcategories',
    viewsets.ProjectConsentCategoryViewSet,
    basename='projectconsentcategory'
)

project_router.register(
    'consents',
    viewsets.ProjectConsentViewSet,
    basename='projectconsent'
)

urlpatterns = [
    path('api/', include(router.urls + project_router.urls)),

    path('create/token/', views.CreateTokenView.as_view(), name='create-project-consent-token'),
    path('sign/<uuid:token>/', views.SignProjectConsentView.as_view(), name='sign-project-consent'),
]
