from django.contrib import admin
from .models import *

from django import forms
from django_ace import AceWidget

class EditorForm(forms.ModelForm):
    input_usable = forms.CharField(widget=AceWidget(width="1000px", height="50px", mode='python'))
    input_shown = forms.CharField(widget=AceWidget(width="1000px", height="50px", mode='python'))
    start_code = forms.CharField(widget=AceWidget(width="1000px", mode='python'))
    solution = forms.CharField(widget=AceWidget(width="1000px", mode='python'))

class EditorFormAdmin(admin.ModelAdmin):
    form = EditorForm

# Register your models here.
admin.site.register(Subject)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Resource)
admin.site.register(Select)
admin.site.register(Text)
admin.site.register(Code, EditorFormAdmin)
admin.site.register(Attempt)
admin.site.register(Answer)
