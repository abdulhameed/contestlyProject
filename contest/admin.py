from django.contrib import admin
from .models import Contest, Contestant, Category


# Register your models here.

class ContestAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'start_date', 'end_date', 'cash_vote', 'vote_cost', 'category')


admin.site.register(Contest, ContestAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag')


admin.site.register(Category, CategoryAdmin)


class ContestantAdmin(admin.ModelAdmin):
    list_display = ('contest', 'contest_id', 'name', 'title', 'post', 'votes', 'created_on',)


admin.site.register(Contestant, ContestantAdmin)
