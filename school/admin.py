from django.contrib import admin
from .models import Attendance,Student,Teacher,Notice

class StudentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Student, StudentAdmin)


class TeacherAdmin(admin.ModelAdmin):
    pass
admin.site.register(Teacher, TeacherAdmin)


class AttendanceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Attendance, AttendanceAdmin)


class NoticeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Notice, NoticeAdmin)
