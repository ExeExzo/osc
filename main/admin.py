from django.contrib import admin
from .models import CamperRegister, Camp, CampParticipant


@admin.register(CamperRegister)
class CamperRegisterAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "iin",
        "birth_date",
        "parent",
        "camp",
        "status",
        "created_at",
    )
    list_filter = ("status", "camp", "birth_date", "created_at")
    search_fields = ("full_name", "iin", "parent__username", "camp__name")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    actions = ["approve_camper", "reject_camper"]

    # кастомные действия для одобрения/отклонения заявки
    def approve_camper(self, request, queryset):
        updated = queryset.update(status="approved")
        self.message_user(request, f"{updated} заявок одобрено.")
    approve_camper.short_description = "Одобрить выбранные заявки"

    def reject_camper(self, request, queryset):
        updated = queryset.update(status="rejected")
        self.message_user(request, f"{updated} заявок отклонено.")
    reject_camper.short_description = "Отклонить выбранные заявки"


@admin.register(Camp)
class CampAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "start_date", "end_date", "capacity", "is_active")
    list_filter = ("is_active", "start_date", "end_date")
    search_fields = ("name", "location")
    ordering = ("-start_date",)


@admin.register(CampParticipant)
class CampParticipantAdmin(admin.ModelAdmin):
    list_display = ("camper", "camp", "start_date", "end_date", "approved_at")
    list_filter = ("camp", "start_date", "end_date")
    search_fields = ("camper__full_name", "camp__name")
    ordering = ("-approved_at",)
    readonly_fields = ("approved_at",)
