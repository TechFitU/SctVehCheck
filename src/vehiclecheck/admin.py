# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.conf.urls import url
from django.forms.models import BaseInlineFormSet
#Resources of import-export app
from import_export import resources

#Clearable input widget for text fields
from clearable_widget import ClearableInput

#django-ajax-selects form and admin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from ajax_select.fields import autoselect_fields_check_can_add

# Register your models here.
from vehiclecheck.models import Cliente, Vehiculo, VerificacionVehiculo, Domicilio, TipoVehiculo,\
        TipoServicio, Estado, Municipio

#Import custom forms
from .forms import ClienteForm, VerificacionVehiculoForm, VerificacionVehiculoCaptchaForm, \
                VehiculoForm, DomicilioForm

class CustomVehiculoInlineFormSet(BaseInlineFormSet):
    def save(self):
        super(CustomVehiculoInlineFormSet, self).save(commit = False)

        #Colocando a cada nueva instancia de Vehiculo que maneja este InlineFormSet,
        #el usuario que lo registra        
        for instance in self.new_objects:
            instance.creado_por = instance.cliente.creado_por
            instance.save()

        super(CustomVehiculoInlineFormSet, self).save()


class VehiculoInline(admin.StackedInline):
    model = Vehiculo
    form = VehiculoForm
    formset = CustomVehiculoInlineFormSet
    fields = (
        ('serie', 'marca', 'modelo', 'anho_modelo',),
        ('placa', 'tarjeta_circulacion','tipo',  'creado_por',),
        ('capacidad_lt', 'capacidad_kg', 'capacidad_personas'),
    
    )
    readonly_fields= ('creado_por',)
    extra=1

class DomicilioStackedInline(admin.StackedInline):
    model = Domicilio
    form = DomicilioForm
    fieldsets = (
        (None, {
            'fields': (
            ('calle', 'numero_exterior', 'numero_interior', 'codigo_postal'),
            ('colonia', 'estado', 'municipio','actual'),)}),
    )

    formfield_overrides = {
        models.CharField: {'widget': ClearableInput}

    }
    extra=1


class ClienteAdmin(admin.ModelAdmin):
    """
    Customize the look of the auto-generated admin for the Persona model
    1. Changing the way in each choice in database is shown
    (new one is in table form, with more than a column)
    2. Displaying the way of adding new question objects,
    including adding new choices inline(TabularInline in this case).
    3. Filtering in "change list" page of Persona, using list_filter
    3. Inserting fieldsets in question forms, with all fields by fieldset
    """
    #Displaying each row in "change list" page, if list_display is not provided,
    #Django will use str() method to display each question,
    #that use our __unicode__() implementation

    list_display = ('complete_name', 'rfc', 'creado',)

    #Adding some search capabilities, searching in all text fields.
    search_fields = ['nombre', 'rfc',]

    #Adding an improvement to the Question change list page: filters using the list_filter.
    #That adds a Filter sidebar that lets people filter the change list by the pub_date field

    list_filter = ['creado']
    fieldsets = (
        ('General', {'fields': (
            ( 'nombre', 'rfc', ),
                                )}),
    )
    #Incluira botones de navegacion para filtrar por rangos de fechas.
    #date_hierarchy = 'creado'

    form = ClienteForm

    inlines = [DomicilioStackedInline, VehiculoInline]

    #Al alcanzar 30 resultados comenzara a paginar
    list_per_page=30

    def save_model(self, request, obj, form, change):
        #Se registra un nuevo cliente (ya sea remitente o destinatario) en el sistema para que pueda autenticarse y
        #tener acceso a sus funcionalidades
        if change is not True:
            obj.creado_por = request.user
            
        obj.save()



class VehiculoAdmin(admin.ModelAdmin):
    """
    Customize the look of the auto-generated admin for the Persona model
    1. Changing the way in each choice in database is shown
    (new one is in table form, with more than a column)
    2. Displaying the way of adding new question objects,
    including adding new choices inline(TabularInline in this case).
    3. Filtering in "change list" page of Persona, using list_filter
    3. Inserting fieldsets in question forms, with all fields by fieldset
    """
    #Displaying each row in "change list" page, if list_display is not provided,
    #Django will use str() method to display each question,
    #that use our __unicode__() implementation

    list_display = ('placa', 'marca', 'serie','anho_modelo','cliente','tipo')

    # list_display_links = ('folio', '')
    # def get_list_display(self, request):
    #     if request.user.is_superuser:
    #         return ('colored_guide_number',  'colored_folio_number','remitente', 'current_state','subtotal','iva','costo_total', 'print_tag','print_ticket','ultima_actualizacion')
    #     elif not request.user.has_perm("paqueteria.check_payment_state"):

    #         return ('colored_guide_number',  'remitente', 'current_state','subtotal','iva','costo_total', 'print_tag','print_ticket','ultima_actualizacion')
    #     else:
    #         return ('colored_guide_number',  'colored_folio_number','remitente', 'current_state','subtotal','iva','costo_total', 'print_tag','print_ticket','ultima_actualizacion')
    
    # #Desplegando el vinculo hacia el objeto remitente mostrado en la change_list de los envios

    # def get_list_display_links(self, request, list_display):
    #     return ('remitente','colored_folio_number','colored_guide_number')
    
    #list_display_links = ('remitente','numero_guia')

    #Adding some search capabilities, searching in all text fields.
    search_fields = ['placa', 'marca','modelo','serie','cliente__nombre']

    #Adding an improvement to the Question change list page: filters using the list_filter.
    #That adds a Filter sidebar that lets people filter the change list by the pub_date field

    list_filter = ['creado', 'tipo']
    
    #Al alcanzar 30 resultados comenzara a paginar
    list_per_page=30

    #Custom form located in forms.py
    form = VehiculoForm

    fields = (
    	('serie', 'marca', 'tarjeta_circulacion', 'anho_modelo',),
    	('placa', 'tipo', 'cliente', 'creado_por',),
        ('capacidad_kg', 'capacidad_lt', 'capacidad_personas', ),
        
    )
    readonly_fields= ('creado_por',)
    #inlines = [VerificacionVehiculoInline]

    def save_model(self, request, obj, form, change):
        #Se registra un nuevo envio en el sistema
        #y luego se le coloca quien lo crea, o sea, el usuario logueado que lo crea       
        
        if change is False:
            obj.creado_por = request.user
        obj.save()




from import_export import fields
class VerificacionVehiculoResource(resources.ModelResource):
    
    #Personalizando un campo en la importacion o exportacion, aqui se muestra la informacion 
    #personalizada del vehiculo

    # vehiculo_completo = fields.Field()
    # def dehydrate_vehiculo_completo(self, obj):
    #    return 'Placa %s, marca %s, modelo %s' % (obj.vehiculo.placa, obj.vehiculo.marca, obj.vehiculo.modelo)

    #Redefinicion del nombre de la columna para cada campo en la exportacion
    no_acreditacion = fields.Field(attribute="no_acreditacion",column_name=u'NÚMERO DE UNIDAD DE VERIFICACIÓN')
    folio = fields.Field(attribute="folio",column_name=u'NÚMERO DE FOLIO DE CERTIFICADO')
    fv_string = fields.Field(attribute="fv_string",column_name=u'FECHA DE VERIFICACIÓN')
    fva_string = fields.Field(attribute="fva_string",column_name=u'FECHA DE VERIFICACIÓN ANTERIOR')
    odometro = fields.Field(attribute="odometro",column_name=u'LECTURA ODÓMETRO')
    vehiculo__cliente__nombre = fields.Field(attribute="vehiculo__cliente__nombre",column_name=u'NOMBRE, RAZÓN O DENOMINACIÓN SOCIAL')
    vehiculo__cliente__rfc = fields.Field(attribute="vehiculo__cliente__rfc",column_name=u'RFC')
    vehiculo__tipo__tipo = fields.Field(attribute="vehiculo__tipo__tipo",column_name=u'TIPO DE VEHÍCULO (1)')
    vehiculo__serie = fields.Field(attribute="vehiculo__serie",column_name=u'NÚMERO DE SERIE O NIV')
    vehiculo__anho_modelo = fields.Field(attribute="vehiculo__anho_modelo",column_name=u'AÑO MODELO')
    vehiculo__marca = fields.Field(attribute="vehiculo__marca",column_name=u'MARCA')
    vehiculo__tipo__numero_ejes = fields.Field(attribute="vehiculo__tipo__numero_ejes",column_name=u'NÚMERO DE EJES')
    vehiculo__placa = fields.Field(attribute="vehiculo__placa",column_name=u'PLACAS')
    vehiculo__tarjeta_circulacion = fields.Field(attribute="vehiculo__tarjeta_circulacion",column_name=u'FOLIO DE LA TARJETA DE CIRCULACIÓN')
    tipo_servicio__codigo = fields.Field(attribute="tipo_servicio__codigo",column_name=u'TIPO DE SERVICIO QUE PRESTA (3)')
    estado_vehiculo = fields.Field(attribute="estado_vehiculo",column_name=u'EL VEHÍCULO SE PRESENTÓ (4)')
    tecnico_verificador = fields.Field(attribute="tecnico_verificador",column_name=u'NOMBRE DEL TÉCNICO QUE VERIFICÓ')
    resultado = fields.Field(attribute="resultado",column_name=u'RESULTADO')
    capacidad_lt = fields.Field(attribute="vehiculo__capacidad_lt",column_name=u'CAPACIDAD (Lt)')
    capacidad_kg = fields.Field(attribute="vehiculo__capacidad_kg",column_name=u'CAPACIDAD (Kg)')
    capacidad_personas = fields.Field(attribute="vehiculo__capacidad_personas",column_name=u'CAPACIDAD (Personas)')

    class Meta:
        model = VerificacionVehiculo
        fields = ('no_acreditacion', 'folio' ,'resultado','fv_string',\
                'fva_string','tecnico_verificador','odometro',\
                'vehiculo__cliente__nombre','vehiculo__cliente__rfc', 'vehiculo__tipo__tipo',\
                'vehiculo__serie','vehiculo__anho_modelo', 'vehiculo__marca','vehiculo__tipo__numero_ejes',\
                'capacidad_kg', 'capacidad_lt','capacidad_personas','vehiculo__placa',\
                'vehiculo__tarjeta_circulacion','tipo_servicio__codigo','estado_vehiculo')
        export_order = ('no_acreditacion', 'folio', 'fv_string', 'fva_string', \
                    'odometro','vehiculo__cliente__nombre', 'vehiculo__cliente__rfc','vehiculo__tipo__tipo',\
                    'vehiculo__serie','vehiculo__anho_modelo', 'vehiculo__marca',\
                    'capacidad_kg', 'capacidad_lt','capacidad_personas','vehiculo__tipo__numero_ejes',\
                    'vehiculo__placa','vehiculo__tarjeta_circulacion','tipo_servicio__codigo',\
                    'estado_vehiculo','tecnico_verificador','resultado'
                    )
        
        widgets = {
                'fecha_verificacion_anterior': {'format': '%d/%m/%Y'},
                'fecha_verificacion': {'format': '%d/%m/%Y'},
                }
        skip_unchanged = True #Saltar los registros importados que no tienen cambios respecto a tabla
        report_skipped = True #True haria que se no muestren los registros sin cambios que se importan


from io import BytesIO
import requests
from import_export.admin import ImportExportModelAdmin

class VerificacionVehiculoAdmin(ImportExportModelAdmin):
    #Camino a la plantilla personalizada

    #change_list_template = 'admin/vehiclecheck/verificacionvehiculo/change_list.html'

    resource_class = VerificacionVehiculoResource
    readonly_fields= ('creado_por', )

    def generate_arrastre_report(self, request, identificador):        
        #Path to report rest service, including format an rute to custom report
        url = 'http://127.0.0.1:8080/jasperserver/rest_v2/reports/reports/Verificaciones/reporte_arrastre.pdf'
         
        #Authorisation credentials:
        auth = ('cliente', '!"#Verificaciones')
         
        #initialize data. Requests will handle encoding.
        data = {"identificador": identificador }
       
        #making a get request straight from documentation
        r = requests.get(url=url, params=data, auth=auth, timeout=15)
         
        #to see request status code do
        #print r.status_code
         
        #will raise HTTP error if there is one:
        r.raise_for_status()
 
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="reporte.pdf"'

        #Buffer en el que se escribira la data generada por el reportador JasperReports Server
        output_buffer = BytesIO()
        output_buffer.write(r.content)
        pdf = output_buffer.getvalue()
        output_buffer.close()
        
        response.write(pdf)
        return response

    def generate_movil_report(self, request, identificador):        
        #Path to report rest service, including format an rute to custom report
        url = 'http://127.0.0.1:8080/jasperserver/rest_v2/reports/reports/Verificaciones/reporte_motriz.pdf'
         
        #Authorisation credentials for the user that connects to the reports server 
        auth = ('cliente', '!"#Verificaciones')
         
        #initialize data. Requests will handle encoding.
        data = {"identificador": identificador }
       
        #making a get request straight from documentation
        r = requests.get(url=url, params=data, auth=auth, timeout=15)
         
        #to see request status code do
        #print r.status_code
         
        #will raise HTTP error if there is one:
        r.raise_for_status()
 
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'filename="reporte.pdf"'

        #Buffer en el que se escribira la data generada por el reportador JasperReports Server
        output_buffer = BytesIO()
        output_buffer.write(r.content)
        pdf = output_buffer.getvalue()
        output_buffer.close()
        
        response.write(pdf)
        return response


    def get_urls(self):
        urls = super(VerificacionVehiculoAdmin, self).get_urls()
        my_urls = [     
            
            url(r'^arrastre_report/(?P<identificador>[0-9]+)/$', \
                self.admin_site.admin_view(self.generate_arrastre_report), \
                name="show_arrastre_report"),
                        
            url(r'^movil_report/(?P<identificador>[0-9]+)/$', \
                self.admin_site.admin_view(self.generate_movil_report), \
                name="show_movil_report"),

            url(r'^export_founded_verification/$', \
                self.admin_site.admin_view(self.export_founded_verification), \
                name="export_founded_verification"),

        ]
        return my_urls + urls


    def export_founded_verification(self, request):
        #Busqueda de las verificaciones en el rango de fechas
        fecha_init = request.POST.get('fecha_inicio',None)
        fecha_end = request.POST.get('fecha_fin',None)
        results = VerificacionVehiculo.objects.filter(fecha_verificacion__gte = fecha_init, fecha_verificacion__lte = fecha_end ).order_by('fecha_verificacion','folio')
        
        #Exportacion de los datos
        dataset = VerificacionVehiculoResource().export(results)
        

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'filename="Verificaciones-Filtradas.xls"'

        #Buffer en el que se escribira la data generada por el reportador JasperReports Server
        output_buffer = BytesIO()
        output_buffer.write(dataset.xls)
        excel = output_buffer.getvalue()
        output_buffer.close()
        
        response.write(excel)
        return response

    def get_fields(self,request, obj=None):
        if obj is None:
            return (
        	   ('folio','no_aprobacion', 'no_acreditacion','vehiculo'),
               ('tipo_servicio','estado_vehiculo', 'odometro','fecha_verificacion_anterior',),
               ('fecha_verificacion','hora_inicio', 'hora_fin', 'observaciones'),
               ('semestre', 'resultado','tecnico_verificador','creado_por',)
            )
        else:
            return (
               ('folio','no_aprobacion', 'no_acreditacion','vehiculo'),
               ('tipo_servicio','estado_vehiculo', 'odometro','fecha_verificacion_anterior',),
               ('fecha_verificacion','hora_inicio', 'hora_fin', 'observaciones'),
               ('semestre', 'resultado','tecnico_verificador','creado_por',)
            )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['verification_id'] = object_id
        return super(VerificacionVehiculoAdmin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)

    def get_queryset(self, request):
        qs = super(VerificacionVehiculoAdmin, self).get_queryset(request)
        fecha_init = request.POST.get('fecha_inicio',None)
        fecha_end = request.POST.get('fecha_fin',None)

        if fecha_init is not None:
            qs = qs.filter(fecha_verificacion__gte = fecha_init)
        if fecha_end is not None:
            qs = qs.filter(fecha_verificacion__lte = fecha_end)
        return qs

    
    list_display = ('colored_folio_number', 'get_placa', 'fecha_verificacion', \
                    'fecha_verificacion_anterior', 'get_cliente', 'get_tipo_vehiculo',\
                    'get_serie_vehiculo', 'get_anho_modelo', 'get_marca_vehiculo')
    #That adds a Filter sidebar that lets people filter the change list by the pub_date field
    list_filter = ['resultado','vehiculo__tipo','tipo_servicio','estado_vehiculo','fecha_verificacion']
    #Al alcanzar 30 resultados comenzara a paginar

    #date_hierarchy = 'creado'
    
    list_per_page=30
    readonly_fields = ('no_aprobacion', 'no_acreditacion', 'creado_por',)
    #Adding some search capabilities, searching in all text fields.
    search_fields = ['folio', 'no_aprobacion','no_acreditacion',\
                    'vehiculo__placa','vehiculo__marca', 'vehiculo__modelo','vehiculo__serie',
                    'vehiculo__tarjeta_circulacion','vehiculo__cliente__nombre']

    
    #inlines = [VerificacionVehiculoInline]

    def save_model(self, request, obj, form, change):
        #Se registra una nueva verificacion en el sistema
        #y luego se le coloca quien lo crea, o sea, el usuario logueado que lo crea        
        if change is False:
            obj.creado_por = request.user

        if obj.fecha_verificacion_anterior is None:
            obj.fecha_verificacion_anterior = timezone.now().date()

        if obj.fecha_verificacion is None:
            obj.fecha_verificacion = timezone.now().date()

        obj.fv_string = obj.fecha_verificacion.strftime("%d/%m/%Y")
        obj.fva_string = obj.fecha_verificacion_anterior.strftime("%d/%m/%Y")
        obj.hi_string = obj.hora_inicio.strftime("%H:%M")
        obj.hf_string = obj.hora_fin.strftime("%H:%M")

        obj.save()

    def get_form(self, request, obj=None, **kwargs):
        # if obj is None:
        #     kwargs['form'] = VerificacionVehiculoCaptchaForm
        # else:
        #     kwargs['form'] = VerificacionVehiculoForm

        kwargs['form'] = VerificacionVehiculoForm
        #autoselect_fields_check_can_add(kwargs['form'], self.model, request.user)
        return super(VerificacionVehiculoAdmin, self).get_form(request, obj, **kwargs)


import adminactions.actions as actions
from django.contrib.admin import site

from django.db import ProgrammingError, OperationalError

from globalconfig.models import SiteConfiguration

try:
    config = SiteConfiguration.get_solo()
except (ProgrammingError, OperationalError):
    config = SiteConfiguration()
    config.empresa = "Non-established"
    config.nombre_sitio = "Non-established"

admin.site_header = u'%s' % config.empresa
admin.site_title = u"%s" % config.nombre_sitio
admin.index_title = u"%s" % config.nombre_sitio

admin.site.register(Cliente, ClienteAdmin)
#admin.register(User, UserAdmin)
#admin.register(Group, GroupAdmin)
admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(VerificacionVehiculo, VerificacionVehiculoAdmin)
admin.site.register(TipoServicio)
admin.site.register(TipoVehiculo)
admin.site.register(Estado)
# register all adminactions (export to csv, export to xls, mass update, etc)
actions.add_to_site(site)