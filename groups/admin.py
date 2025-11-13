from django.contrib import admin
from .models import Course, Topic, StudyGroup, Membership

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')
    search_fields = ('code', 'title')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 0

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'room', 'meeting_time', 'created_by', 'created_at')
    list_filter = ('course', 'topics')
    search_fields = ('title', 'room', 'description')
    inlines = [MembershipInline]

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'role', 'status', 'created_at')
    list_filter = ('status', 'role')
    search_fields = ('user__username', 'group__title')
