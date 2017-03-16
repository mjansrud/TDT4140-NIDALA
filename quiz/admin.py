from django import forms
from django.contrib import admin
from django_ace import AceWidget
from django.forms import ModelForm, TextInput
from suit.widgets import NumberInput, AutosizedTextarea

from .models import *


class EditorForm(forms.ModelForm):
    input_usable = forms.CharField(widget=AceWidget(mode='python'))
    input_shown = forms.CharField(widget=AceWidget(mode='python'))
    start_code = forms.CharField(widget=AceWidget(mode='python'))
    solution = forms.CharField(widget=AceWidget(mode='python'))

class EditorFormAdmin(admin.ModelAdmin):
    def get_model_perms(self, request): return {}
    form = EditorForm

class ResourceInline(admin.TabularInline):
    show_change_link = True
    model = Resource
    extra = 1
    exclude = ['description']
    suit_classes = 'suit-tab suit-tab-resources'

class TextInline(admin.TabularInline):
    show_change_link = True
    model = Text
    max_num = 1
    suit_classes = 'suit-tab suit-tab-text'

class SelectInline(admin.TabularInline):
    show_change_link = True
    model = Select
    exclude = ['description']
    suit_classes = 'suit-tab suit-tab-selects'

class CodeInline(admin.StackedInline):
    show_change_link = True
    model = Code
    form = EditorForm
    max_num = 1
    suit_classes = 'suit-tab suit-tab-code'

class QuestionForm(ModelForm):
    class Meta:
        widgets = {
            'order': NumberInput(attrs={'class': 'input-mini'}),
            'attempts':  NumberInput(attrs={'class': 'input-mini'}),
        }

class QuestionAdmin(admin.ModelAdmin):
    def get_model_perms(self, request): return {}
    form = QuestionForm
    inlines = [
        TextInline,
        CodeInline,
        SelectInline,
        ResourceInline
    ]

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-question'),
            'fields': ['title', 'description', 'type', 'order', 'attempts', 'quiz']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-selects'),
            'fields': [],
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-text'),
            'fields': [],
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-code'),
            'fields': [],
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-resources'),
            'fields': [],
        })
    ]

    suit_form_tabs = (('question', 'Question'), ('selects', 'Selects'), ('text', 'Text'), ('code', 'Code'), ('resources', 'Resources'))
    suit_classes = 'suit-tab suit-tab-question'

class QuestionInline(admin.TabularInline):
    show_change_link = True
    model = Question
    form = QuestionForm
    extra = 1
    exclude = ['description']
    suit_classes = 'suit-tab suit-tab-questions'

class AttemptInLine(admin.TabularInline):
    show_change_link = True
    model = Attempt
    extra = 0
    suit_classes = 'suit-tab suit-tab-attempts'

class QuizForm(ModelForm):
    class Meta:
        widgets = {
            'exercise_number': NumberInput(attrs={'class': 'input-mini'}),
            'pass_percent': NumberInput(attrs={'class': 'input-mini'}),
            'attempts':  NumberInput(attrs={'class': 'input-mini'}),
        }

class QuizAdmin(admin.ModelAdmin):
    def get_model_perms(self, request): return {}
    form = QuizForm
    inlines = [
        QuestionInline,
        AttemptInLine
    ]
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-quiz'),
            'fields': ['title', 'description', 'exercise_number', 'attempts', 'pass_percent', 'subject']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-questions'),
            'fields': [],
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-attempts'),
            'fields': [],
        })
    ]

    suit_form_tabs = (('quiz', 'Quiz'), ('questions', 'Questions'), ('attempts', 'Attempts'))
    suit_classes = 'suit-tab suit-tab-quiz'


class QuizInline(admin.TabularInline):
    show_change_link = True
    model = Quiz
    form = QuizForm
    extra = 1
    exclude = ['description']
    suit_classes = 'suit-tab suit-tab-quiz'

class SubjectAdmin(admin.ModelAdmin):
    inlines = [
        QuizInline
    ]

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-subject'),
            'fields': ['code', 'title', 'syllabus']
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-quiz'),
            'fields': [],
        })
    ]

    suit_form_tabs = (('subject', 'Subjects'), ('quiz', 'Quizes'))
    suit_classes = 'suit-tab suit-tab-subject'


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
