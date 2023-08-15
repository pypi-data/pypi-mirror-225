'''
URL configuration for budgetmanager app
'''
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'budgetmanager'  # pylint: disable=invalid-name
router = DefaultRouter()
router.register(r'budget', views.BudgetViewSet)
router.register(r'share', views.BudgetShareViewSet)
router.register(r'payee', views.PayeeViewSet)
router.register(r'payment', views.PaymentViewSet)

urlpatterns = router.urls + [
    path('total/', views.TotalView.as_view()),
]
