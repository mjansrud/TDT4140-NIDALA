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
    form = EditorForm


class TextInline(admin.TabularInline):
    model = Text


class SelectInline(admin.TabularInline):
    model = Select


class CodeInline(admin.TabularInline):
    model = Code


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        TextInline,
        SelectInline,
        CodeInline
    ]


class QuestionInline(admin.TabularInline):
    model = Question
    show_change_link = True


class QuizAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline
    ]


class QuizInline(admin.TabularInline):
    model = Quiz
    show_change_link = True


class SubjectAdmin(admin.ModelAdmin):
    inlines = [
        QuizInline
    ]


# Register your models here.

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Resource)
admin.site.register(Select)
admin.site.register(Text)
admin.site.register(Code, EditorFormAdmin)
admin.site.register(Attempt)
admin.site.register(Answer)
