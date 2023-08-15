'''Admin setup for budgetmanager app'''
from django.contrib import admin
from . import models


@admin.register(models.Budget)
class BudgetAdmin(admin.ModelAdmin):
    '''Settings for the Budget admin'''
    list_display = ('user', 'name', 'active')
    list_display_links = list_display
    list_filter = ('user', 'active')
    sortable_by = list_display
    search_fields = ('name',)
    search_help_text = 'Search by budget name'
    list_per_page = 20


@admin.register(models.BudgetShare)
class BudgetShareAdmin(admin.ModelAdmin):
    '''Settings for the BudgetShare admin'''
    list_display = ('user', 'budget', 'can_edit')
    list_display_links = list_display
    list_filter = list_display
    sortable_by = list_display
    readonly_fields = ('user', 'budget')
    list_per_page = 20

    def get_readonly_fields(self, request, obj=...):
        if obj is None:
            return tuple()
        return self.readonly_fields


@admin.register(models.Payee)
class PayeeAdmin(admin.ModelAdmin):
    '''Settings form the Payee admin'''
    list_display = ('budget', 'name')
    list_display_links = list_display
    list_filter = ('budget',)
    sortable_by = list_display
    search_fields = ('name',)
    search_help_text = 'Search by payee name'
    list_per_page = 20


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    '''Settings for the Payment admin'''
    date_hierarchy = 'date'
    list_display = ('payee', 'date')
    list_display_links = list_display
    list_filter = ('payee', 'date')
    sortable_by = list_display
    list_per_page = 20
