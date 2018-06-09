# -*- coding: utf-8 -*-
from django.db import models, ProgrammingError

from django.utils.html import format_html
from smart_selects.db_fields import ChainedForeignKey
from django.conf import settings
# Create your models here.

class Cliente(models.Model):
    nombre = models.CharField(max_length=150, db_index=True, help_text="Persona/Empresa")

    rfc = models.CharField(verbose_name="RFC", max_length=30, db_index=True, null=True, blank=True)
    #tarjeta_circulacion = models.CharField(u"Tarjeta circulación", max_length=25)

    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    creado = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(u"Última actualización",auto_now=True)

    def complete_name(self):
        return "%s" % (self.nombre,)

    complete_name.short_description = "Nombre completo"
    complete_name.admin_order_field = "nombre"

    def __str__(self):
        return u'%s' % (self.nombre,)

    class Meta:
        db_table = "cliente"
        ordering = ['-creado']
        get_latest_by = 'creado'
        verbose_name="cliente"
        verbose_name_plural="clientes"

class Estado(models.Model):
    idestado = models.CharField(primary_key=True, max_length=25)
    nombre = models.CharField(max_length=45)


    def __str__(self):
        return u'%s' % self.nombre

    class Meta:
        db_table = "estado"
        verbose_name="estado"
        verbose_name_plural="estados"

class Municipio(models.Model):
    idmunicipio = models.IntegerField(primary_key=True)
    idestado = models.ForeignKey(Estado, db_column="idestado", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return u'%s' % self.nombre

    class Meta:
        db_table = "municipio"
        verbose_name="municipio"
        verbose_name_plural="municipios"
        #unique_together = ('nombre', 'estado')


class Domicilio(models.Model):
    """
    Clase Domicilio, un cliente tendra muchos o un solo domicilio.
    A la hora de efectuar el chequeo del vehiculo debe pasar la direccion específica.
    """
    calle = models.CharField(max_length=120, null=True, blank=True)
    numero_interior = models.CharField(verbose_name="Número interior", default="S/N", max_length = 10 )
    numero_exterior = models.CharField("Número exterior", default="S/N", max_length = 10)
    colonia = models.CharField(max_length=100, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)
    municipio = ChainedForeignKey(
        Municipio,
        chained_field="estado",
        chained_model_field="idestado",
        show_all=True,
        auto_choose=True
    )
    # estado = models.CharField(max_length=30, choices=(
    #     ('TAMAULIPAS', 'TAMAULIPAS'),
    #     ('NUEVO LEÓN', 'NUEVO LEÓN'),
    #     ('DF', 'DISTRITO FEDERAL'),
    #     ('DISTRITO FEDERAL', 'AGUASCALIENTES'),
    #     ('BAJA CALIFORNIA NORTE', 'BAJA CALIFORNIA NORTE'),
    #     ('BAJA CALIFORNIA SUR', 'BAJA CALIFORNIA SUR'),
    #     ('CAMPECHE', 'CAMPECHE'),
    #     ('COAHUILA', 'COAHUILA'),
    #     ('COLIMA', 'COLIMA'),
    #     ('CHIAPAS', 'CHIAPAS'),
    #     ('CHIHUAHUA', 'CHIHUAHUA'),
    #     ('DURANGO', 'DURANGO'),
    #     ('GUANAJUATO', 'GUANAJUATO'),
    #     ('GUERRERO', 'GUERRERO'),
    #     ('HIDALGO', 'HIDALGO'),
    #     ('JALISCO', 'JALISCO'),
    #     ('ESTADO DE MÉXICO', 'ESTADO DE MÉXICO'),
    #     ('MICHOACÁN', 'MICHOACÁN'),
    #     ('MORELOS', 'MORELOS'),
    #     ('NAYARIT', 'NAYARIT'),
    #     ('OAXACA', 'OAXACA'),
    #     ('PUEBLA', 'PUEBLA'),
    #     ('QUERÉTARO', 'QUERÉTARO'),
    #     ('QUINTANA ROO', 'QUINTANA ROO'),
    #     ('SAN LUIS POTOSÍ', 'SAN LUIS POTOSÍ'),
    #     ('SINALOA', 'SINALOA'),
    #     ('SONORA', 'SONORA'),
    #     ('TABASCO', 'TABASCO'),
    #     ('TLAXCALA', 'TLAXCALA'),
    #     ('YUCATÁN', 'YUCATÁN'),
    #     ('ZACATECAS', 'ZACATECAS')
    # ), default="TAMAULIPAS"
    # )
    actual = models.BooleanField(default=True)
    #municipio = models.CharField(max_length=100, null=True, blank=True)
    codigo_postal = models.IntegerField("Código postal:", null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Domicilio, self).save(*args, **kwargs) # Call the "real" save() method.

        if self.actual is True:
            domicilios_by_cliente = Domicilio.objects.filter(cliente_id = self.cliente.id).exclude(pk=self.id)

            domicilios_by_cliente.update(actual = False)

    def __str__(self):
        return u"%s, %s , %s" % (self.calle, self.municipio, self.estado)

    class Meta:
        db_table = "domicilio"
        verbose_name="Domicilio"
        verbose_name_plural="Domicilios"

class TipoVehiculo(models.Model):
    codigo = models.CharField(u"Código", max_length=10, unique=True)
    tipo = models.CharField(u"Tipo", max_length=50, unique=True)
    numero_ejes = models.IntegerField(u"No. Ejes", blank=True, null=True)

    def __str__(self):
        return u"%s" % (self.tipo, )
    class Meta:
        db_table = "tipovehiculo"
        verbose_name=u"Tipo de vehículo"
        verbose_name_plural=u"Tipos de vehículos"

class TipoServicio(models.Model):
    nombre = models.CharField("Nombre tipo", max_length=150, unique=True)
    codigo = models.CharField(u"Código", max_length=5, unique=True)
    def __str__(self):
        return u"%s" % (self.nombre,)
    class Meta:
        db_table = "tiposervicio"
        verbose_name=u"Tipo de servicio"
        verbose_name_plural=u"Tipos de servicio"



class Vehiculo(models.Model):
    placa = models.CharField("Placas", max_length=25)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(null=True, blank=True, max_length=25)
    anho_modelo = models.IntegerField(u"Año modelo")
    serie = models.CharField("No. Serie o NIV", max_length=25, primary_key=True)
    tipo = models.ForeignKey(TipoVehiculo, verbose_name=u"Tipo de Vehículo", on_delete=models.SET_NULL, null=True)
    capacidad_kg = models.IntegerField("Capacidad (kg)", default=0)
    capacidad_lt = models.IntegerField("Capacidad (litros)", default=0)
    capacidad_personas = models.IntegerField("Capacidad (pasajeros)", default=0)
    tarjeta_circulacion = models.CharField(u"Tarjeta circulación", max_length=25, default="N/A")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=0)
    creado = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(u"Última actualización",auto_now=True)


    def __str__(self):
        return u"Marca %s, año %s, placa %s" % (self.marca, self.anho_modelo, self.placa)

    class Meta:
        db_table = "vehiculo"
        ordering = ['-creado']
        get_latest_by = 'creado'
        #unique_together = (("nombre", "apellidos",),)
        verbose_name=u"Vehículo"
        verbose_name_plural=u"Vehículos"


from globalconfig.models import SiteConfiguration
from django.utils import timezone
class VerificacionVehiculo(models.Model):
    def __init__(self):
        super(VerificacionVehiculo, self).__init__()
        try:
            self.no_aprobacion = SiteConfiguration.get_solo().no_aprobacion
        except ProgrammingError:
            self.no_aprobacion = ""

        try:
            self.no_acreditacion = SiteConfiguration.get_solo().no_acreditacion
        except ProgrammingError:
            self.no_acreditacion = ""

    RESULTADOS_DICT ={
        "APROBADO": "APROBADO",
        "CANCELADO": "CANCELADO",
        "RECHAZADO": "RECHAZADO"
    }

    ESTADO_VEHICULO_DICT = {
        "V": u"VACÍO",
        "C": "CARGADO",
    }


    folio = models.CharField(default="desconocido", max_length=15, unique=True)
    no_aprobacion = models.CharField(u"No. Aprobación", max_length=25)
    no_acreditacion = models.CharField(u"No. Acreditación", max_length=25)
    semestre = models.CharField(max_length=1, choices=(
        ("1","1"),
        ("2","2"),
        ), default="1")
    resultado = models.CharField(choices=RESULTADOS_DICT.items(),default="CANCELADO", max_length=10)
    tipo_servicio = models.ForeignKey(TipoServicio, verbose_name="Tipo servicio", on_delete=models.SET_DEFAULT, default="SS")
    estado_vehiculo= models.CharField(u"Estado vehículo",choices=ESTADO_VEHICULO_DICT.items(),default="V", max_length=1)
    observaciones = models.TextField(blank=True)
    odometro = models.CharField("Odómetro",max_length=15, default="N/A", help_text="kilometraje del vehículo")
    fecha_verificacion = models.DateField(verbose_name=u"Fecha verificación")
    fv_string = models.CharField(editable = False, max_length=10, default=str(timezone.now().date()))

    fecha_verificacion_anterior = models.DateField(verbose_name=u"Verificación anterior", null=True, blank=True)
    fva_string = models.CharField(editable = False,max_length=10,  default= str(timezone.now().date()))
    hora_inicio = models.TimeField(verbose_name= u"Hora inicio")
    hi_string = models.CharField(editable = False, max_length=10, default= timezone.now().time().strftime("%H:%M"))
    hora_fin = models.TimeField(verbose_name= u"Hora fin")
    hf_string = models.CharField(editable = False, max_length=10, default= timezone.now().time().strftime("%H:%M"))
    tecnico_verificador = models.CharField(u"Técnico verificador",max_length=75, )
    vehiculo = models.ForeignKey(Vehiculo, on_delete = models.PROTECT)
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    creado = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(u"Última actualización",auto_now=True)

    def get_tipo_servicio(self):
        return self.TIPO_SERVICIO_DICT[self.tipo_servicio]

    def get_resultado(self):
        return self.RESULTADOS_DICT[self.resultado]

    def get_estado_vehiculo(self):
        return self.ESTADO_VEHICULO_DICT[self.estado_vehiculo]

    def colored_folio_number(self):
        return format_html('<span style="color: #{};">{}</span>',
                           "FF953A",
                           self.folio
                           )

    colored_folio_number.allow_tags = True
    colored_folio_number.short_description="Folio"

    def get_cliente(self):
        return self.vehiculo.cliente
    get_cliente.short_description='Cliente'

    def get_tipo_vehiculo(self):
        return self.vehiculo.tipo
    get_tipo_vehiculo.short_description=u'Tipo vehículo'

    def get_placa(self):
        return self.vehiculo.placa
    get_placa.short_description='Placa'

    def get_serie_vehiculo(self):
        return self.vehiculo.serie
    get_serie_vehiculo.short_description='Serie'

    def get_anho_modelo(self):
        return self.vehiculo.anho_modelo
    get_anho_modelo.short_description=u'Año'

    def get_marca_vehiculo(self):
        return self.vehiculo.marca
    get_marca_vehiculo.short_description=u'Marca'

    def get_absolute_url(self):
        from django.urls.base import reverse
        return reverse('vehiclecheck:show_verification', kwargs={'identificador': str(self.id)})

    def __str__(self):
        return u"Verificación con folio %s del vehículo %s" % (self.folio,self.vehiculo)

    class Meta:
        db_table = "verificacion"
        ordering = ['-fecha_verificacion']
        get_latest_by = 'fecha_verificacion'
        #unique_together = (("nombre", "ap_paterno", "ap_materno"),)
        verbose_name=u"Verificación vehicular"
        verbose_name_plural="Verificaciones vehiculares"
