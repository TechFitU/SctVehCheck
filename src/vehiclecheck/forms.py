# -*- coding: utf-8 -*-
from django.forms import ModelForm, ValidationError
from clearable_widget import ClearableInput
import django.forms as forms
#from captcha.fields import CaptchaField
#Import custom models here
from .models import Vehiculo, VerificacionVehiculo, Cliente, Domicilio


#Custom widgets for some form fields
from .widgets import DateWidget, CustomCheckBoxWidget, TimeWidget

#Import make_ajax_field helper to build an ajax form field 
from ajax_select import make_ajax_field
#Custom widgets for some form fields
class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"
        localized_fields = "__all__"

class DomicilioForm(ModelForm):
    class Meta:
        model = Domicilio
        fields = "__all__"
        localized_fields = "__all__"
        widgets ={
            'actual': CustomCheckBoxWidget(),
        }

class VerificacionVehiculoCaptchaForm(ModelForm):
    #captcha = CaptchaField()

    class Meta:
        model = VerificacionVehiculo
        fields = "__all__"
        localized_fields = "__all__"

    vehiculo  = make_ajax_field(VerificacionVehiculo, 'vehiculo', 'vehiculo', \
        help_text="Buscar por cualquier dato del vehículo", \
        plugin_options = {'autoFocus': True, 'minLength': 4})

class VerificacionVehiculoForm(ModelForm):
    class Meta:
        model = VerificacionVehiculo
        fields = "__all__"
        localized_fields = "__all__"

        widgets ={
            'fecha_verificacion': DateWidget(),
            'fecha_verificacion_anterior': DateWidget(),
            'hora_inicio': TimeWidget(),
            'hora_fin': TimeWidget()
            

        }
   
    vehiculo  = make_ajax_field(VerificacionVehiculo, 'vehiculo', 'vehiculo', \
        help_text="Buscar por cualquier dato del vehículo", \
        plugin_options = {'autoFocus': True, 'minLength': 4})


class VehiculoForm(ModelForm):
    class Meta:
        model = Vehiculo
        fields = "__all__"
        localized_fields = "__all__"

        widgets ={
            'nombre': ClearableInput(),
            'apellidos': ClearableInput(),
            'rfc': ClearableInput(),

        }
    
    cliente  = make_ajax_field(Vehiculo, 'cliente', 'cliente', \
        help_text="Buscar nombre, apellidos, rfc del cliente", \
        plugin_options = {'autoFocus': True, 'minLength': 4})