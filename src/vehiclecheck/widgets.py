# -*- coding: utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

class DateWidget(forms.DateInput):
    def __init__(self, attrs={}):

        attrs = {
            "data-beatpicker": "true",
            "data-beatpicker-module": "clear, gotoDate",
            "data-beatpicker-position": "['*','*']",
            "data-beatpicker-format": "['YYYY','MM','DD'],separator:'-'",
            
        }
        super(DateWidget, self).__init__(attrs)

    class Media:
        extend = False  # No extiende las definiciones de javascripts ni css de su clase padre
        css = {
            'all': ('admin/css/Beatpicker.min.css',)
        }
        js = ('admin/js/Beatpicker.min.js', )


class CustomCheckBoxWidget(forms.CheckboxInput):
    def __init__(self, attrs={}):        
        super(CustomCheckBoxWidget, self).__init__(attrs)

    def render (self, name, value, attrs=None):
        
        if value is True:
            output = (u'<div class="btn-group" data-toggle="buttons"><label class="btn btn-info active"><input type="checkbox" checked name="%s" autocomplete="off"><span class="glyphicon glyphicon-ok"></span></label></div>' % (name, ),)
        else:
            output = (u'<div class="btn-group" data-toggle="buttons"><label class="btn btn-info"><input type="checkbox" name="%s" autocomplete="off"><span class="glyphicon glyphicon-ok"></span></label></div>' % (name, ),)
        
        return mark_safe(u''.join(output))

    class Media:
        extend = False  # No extiende las definiciones de javascripts ni css de su clase padre
        css = {
            'all': ('admin/css/customcheckbox.css',)
        }


class TimeWidget(forms.TextInput):
    def __init__(self, attrs={}):

        attrs = {
            "class": "timepicker",
        }
        super(TimeWidget, self).__init__(attrs)

    class Media:
        extend = False  # No extiende las definiciones de javascripts ni css de su clase padre
        css = {
            'all': ('admin/css/timepicki.css',)
        }
        js = ('admin/js/timepicki.js', )

