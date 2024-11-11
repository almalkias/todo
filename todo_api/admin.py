from django.contrib import admin
from .models import CustomUser, Task, Category
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_completed', 'priority', 'category', 'created_at', 'updated_at')


admin.site.register(Task, TaskAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Category)
