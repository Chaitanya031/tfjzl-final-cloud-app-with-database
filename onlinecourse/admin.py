from django.contrib import admin
from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Question,
    Choice,
    Submission
)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 5


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 5


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'course', 'grade')
    list_filter = ('course',)
    search_fields = ('question_text',)
    inlines = [ChoiceInline]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'pub_date', 'total_enrollment')
    list_filter = ('pub_date',)
    search_fields = ('name',)
    inlines = [QuestionInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)
    inlines = [QuestionInline]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'pub_date', 'total_enrollment')
    list_filter = ('pub_date',)
    search_fields = ('name',)
    inlines = [LessonInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)

