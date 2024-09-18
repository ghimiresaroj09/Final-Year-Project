from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

admin.site.site_header = "Hamro Agro Farm"
admin.site.site_title = "Hamro Agro Farm"
admin.site.index_title = "Welcome Admin"

# Inline profile model in the user admin
class ProfileInline(admin.StackedInline):
    model = Profile
    exclude = ('old_cart',)
    can_delete = False

# Extend User Model with sections
class UserAdmin(BaseUserAdmin):
    model = User

    # Group fields into sections
    fieldsets = (
        ("Basic Information", {
            'fields': ('username', 'first_name', 'last_name', 'email', 'password')
        }),
        ("Permissions", {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),  # Makes this section collapsible
        }),
        ("Important Dates", {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),  # Makes this section collapsible
        }),
    )

    # Adding inline profile
    inlines = [ProfileInline]

    # Configuring the list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name')
    list_per_page = 10

    # Make some fields read-only
    readonly_fields = ('username', 'email', 'last_login', 'date_joined')

# ProfileAdmin for Profile model
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address',)
    search_fields = ('user__username', 'phone')
    list_per_page = 10
    exclude = ('old_cart',)

# Unregister the default User model
admin.site.unregister(User)

# Register the extended User model and Profile
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
