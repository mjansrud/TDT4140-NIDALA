from django import forms
from django.contrib import admin
from django_ace import AceWidget

from .models import *


class EditorForm(forms.ModelForm):
    input_usable = forms.CharField(widget=AceWidget(width="1000px", height="50px", mode='python'))
    input_shown = forms.CharField(widget=AceWidget(width="1000px", height="50px", mode='python'))
    start_code = forms.CharField(widget=AceWidget(width="1000px", mode='python'))
    solution = forms.CharField(widget=AceWidget(width="1000px", mode='python'))

class EditorFormAdmin(admin.ModelAdmin):
    def get_model_perms(self, request): return {}
    form = EditorForm

class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1

class TextInline(admin.TabularInline):
    model = Text
    max_num = 1

class SelectInline(admin.TabularInline):
    model = Select

class CodeInline(admin.TabularInline):
    show_change_link = True
    model = Code
    max_num = 1

class QuestionAdmin(admin.ModelAdmin):
    def get_model_perms(self, request): return {}
    inlines = [
        TextInline,
        CodeInline,
        SelectInline,
        ResourceInline
    ]

class QuestionInline(admin.TabularInline):
    show_change_link = True
    model = Question
    extra = 1

class AttemptInLine(admin.TabularInline):
    show_change_link = True
    model = Attempt
    extra = 0

class QuizAdmin(admin.ModelAdmin):
    def get_model_perms(self, request): return {}
    inlines = [
        QuestionInline,
        AttemptInLine
    ]

class QuizInline(admin.TabularInline):
    show_change_link = True
    model = Quiz
    extra = 1

class SubjectAdmin(admin.ModelAdmin):
    inlines = [
        QuizInline
    ]

class AnswersInline(admin.TabularInline):
    show_change_link = True
    model = Answer
    extra = 0

class AttemptAdmin(admin.ModelAdmin):
    def get_model_perms(self, request): return {}
    inlines = [
        AnswersInline
    ]

# Register your models here.
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Code, EditorFormAdmin)
admin.site.register(Attempt, AttemptAdmin)
#admin.site.register(Resource)
#admin.site.register(Select)
#admin.site.register(Text)
#admin.site.register(Answer)
