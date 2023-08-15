# pylint: disable=unused-argument
from rest_framework.permissions import BasePermission


class IsBudgetOwner(BasePermission):
    def has_obj_permission(self, request, view, obj):
        return obj.user == request.user


class CanAccessBudgetShare(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.budget.user == request.user


class IsPayeeOwner(BasePermission):
    def has_obj_permission(self, request, view, obj):
        return obj.budget.user == request.user


class IsPaymentOwner(BasePermission):
    def has_obj_permission(self, request, view, obj):
        return obj.payee.budget.user == request.user
